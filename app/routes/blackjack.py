from fastapi import APIRouter, Body, Depends

import app.service.blackjack as blackjack_service
import app.service.user as user_service

router = APIRouter(prefix="/blackjack", tags=["Blackjack"])


@router.get("/game", response_model=blackjack_service.BlackjackGame)
async def get_game(game_id: str):
    return await blackjack_service.get_game(game_id)


@router.get("/game/all")
async def find_all_created_game():
    return await blackjack_service.find_all_created_game()


@router.post("/create")
async def create_game(user=Depends(user_service.manager), name: str = Body()):
    return await blackjack_service.create_game(user, name)


@router.post("/enter")
async def enter_game(user=Depends(user_service.manager), game_id: str = Body()):
    return await blackjack_service.enter_game(user, game_id)


@router.post("/ready")
async def ready_game(user=Depends(user_service.manager), game_id: str = Body()):
    return await blackjack_service.ready(user, game_id)


@router.post("/ready/undo")
async def undo_ready_game(user=Depends(user_service.manager), game_id: str = Body()):
    return await blackjack_service.undo_ready(user, game_id)


@router.post("/bet")
async def bet_game(user=Depends(user_service.manager), game_id: str = Body(), bet: int = Body()):
    return await blackjack_service.bet(user, game_id, bet)


@router.post("/hit")
async def hit(user=Depends(user_service.manager), game_id: str = Body()):
    return await blackjack_service.hit(user, game_id)


@router.post("/stand")
async def stand(user=Depends(user_service.manager), game_id: str = Body()):
    return await blackjack_service.stand(user, game_id)


@router.post("/double_down")
async def double_down(user=Depends(user_service.manager), game_id: str = Body()):
    return await blackjack_service.double_down(user, game_id)


@router.post("/game/leave")
async def leave_game(user=Depends(user_service.manager), game_id: str = Body()):
    return await blackjack_service.leave_game(user, game_id)
