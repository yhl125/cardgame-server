from beanie import PydanticObjectId
from fastapi import APIRouter, Body
from pydantic import BaseModel

from app.models.sample import Sample
from app.blackjack_comm import send_card, send_hand
router = APIRouter(prefix="/sample", tags=["Sample"])


@router.get("/get_card/")
async def get_single_card(card_value):
    return await card_value


@router.get("/get_hand/")
async def get_sample_by_id(cards):

    return await cards # 리스트를 그대로 보낼 수 있나?


@router.post("", response_model=Sample)
async def create_sample(name: str = Body()):
    """Create sample data"""
    sample = Sample(name=name)
    await sample.insert()
    return sample


class UpdateSample(BaseModel):
    id: str
    name: str


@router.put("")
async def update_sample_by_id(update_input: UpdateSample):
    """Update sample data by id"""
    sample = await Sample.get(PydanticObjectId(update_input.id))
    sample.name = update_input.name
    await sample.save()
    return sample


@router.delete("")
async def delete_sample_by_id(_id: str):
    """Delete sample data by id"""
    sample = await Sample.get(PydanticObjectId(_id))
    await sample.delete()
    return "Successfully deleted"
