import uvicorn
from typing import Optional
from fastapi import FastAPI, HTTPException, Path, status, Query, Depends
from chess_db import AsyncChessGameDB, ChessGame
from user_db import UserDB
from fastapi.security import HTTPBasic, HTTPBasicCredentials

USER_DB = UserDB()
CHESS_DB = AsyncChessGameDB(USER_DB)
app = FastAPI(
    title="Chess Server",
    description="Implementation of a simultaneous multi-game Chess server by Alejandro Martinez."
)
security = HTTPBasic()


async def get_game(game_id: str) -> ChessGame:
    """
    Get a game from the blackjack game database, otherwise raise a 404.

    :param game_id: the uuid in str of the game to retrieve
    """
    the_game = await CHESS_DB.get_game(game_id)
    if the_game is None:
        raise HTTPException(status_code=404, detail=f"Game {game_id} not found.")
    return the_game


@app.get('/')
async def home():
    return {"message": "Welcome to Chess!"}


@app.post('/user/create', status_code=status.HTTP_201_CREATED)
async def create_user(username: str):
    the_username, the_password = USER_DB.create_user(username)
    return {'success': True, 'username': the_username, 'password': the_password}


@app.get('/game/create_game', status_code=status.HTTP_201_CREATED)
async def create_game(credentials: HTTPBasicCredentials = Depends(security)):
    new_uuid, new_term_pass, owner_username = await CHESS_DB.add_game(owner=credentials.username)
    CHESS_DB._current_games_info[new_uuid].players.append(owner_username)
    return {'success': True, 'game_id': new_uuid, 'termination_password': new_term_pass, 'game_owner': owner_username}


@app.post('/game/{game_id}/add_player')
async def add_player_to_game(game_id: str, username: str, credentials: HTTPBasicCredentials = Depends(security)):
    owner, players = await CHESS_DB.game_info(game_id)
    if owner == credentials.username:
        player_idx = await CHESS_DB.add_player(game_id, username)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Must be Owner to Execute Function")
    return {'success': True, 'game_uuid': game_id, 'player_username': username, 'player_idx': player_idx}


@app.get('/game/{game_id}/get_player_idx')
async def get_player_idx(game_id: str, username: str, credentials: HTTPBasicCredentials = Depends(security)):
    owner, players = CHESS_DB.game_info(game_id)
    if USER_DB.is_valid(credentials.username, credentials.password) is True:
        player_idx = players.index(username)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Must be Owner to Execute Function")
    return {'success': True, 'game_id': game_id, 'player_username': credentials.username, 'player_idx': player_idx}


@app.post('/game/{game_id}/initialize')
async def init_game(game_id: str = Path(..., description='the unique game id'),
                    credentials: HTTPBasicCredentials = Depends(security)):
    owner, players = await CHESS_DB.game_info(game_id)
    if credentials.username == owner:
        the_game = await get_game(game_id)
        the_game.board.print_board()
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Must be Owner to Execute Function")
    return {'success': True}


@app.post('/game/{game_id}/player/{player_idx}/{player_move}}', status_code=status.HTTP_401_UNAUTHORIZED)
async def player_move(game_id: str = Path(..., description='the unique game id'),
                      player_idx: int = Path(..., description='the player index (zero-indexed)'),
                      player_move: str = Path(..., description='the players move'),
                      credentials: HTTPBasicCredentials = Depends(security)):
    owner, players = await CHESS_DB.game_info(game_id)
    request_idx = players.index(credentials.username)
    if USER_DB.is_valid(credentials.username, credentials.password):
        if player_idx == request_idx:
            the_game = await get_game(game_id)
            if the_game.get_move(player_idx, player_move):
                the_game.execute_move(player_idx)
                current_move = the_game.move(player_idx)
            else:
                raise HTTPException(status.HTTP_401_UNAUTHORIZED)
        else:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    return {'player': player_idx,
            'current_move': str(current_move),
            'player_stack': the_game.move.current_move()}


@app.get('/game/{game_id}/winners')
async def get_winners(game_id: str = Path(..., description='the unique game id')):
    the_game = await get_game(game_id)
    winner = the_game.who_won()
    return {'game_id': game_id,
            'winner': winner}


@app.post('/game/{game_id}/terminate')
async def delete_game(game_id: str = Path(..., description='the unique game id'),
                      password: str = Query(..., description='the termination password'),
                      credentials: HTTPBasicCredentials = Depends(security)):
    owner, players = await CHESS_DB.game_info(game_id)
    if USER_DB.is_valid(credentials.username, credentials.password):
        if owner == credentials.username:
            the_game = await CHESS_DB.del_game(game_id, password, credentials.username)
            if the_game is False:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Game not found.")
        else:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    return {'success': True, 'deleted_id': game_id}


if __name__ == '__main__':
    # running from main instead of terminal allows for debugger
    # TODO: modify the below to add HTTPS (SSL/TLS) support
    uvicorn.run('web_chess:app', port=8000, log_level='info', reload=True, ssl_keyfile='./keys/private.pem',
                ssl_certfile='./keys/public.pem')
