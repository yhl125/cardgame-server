from beanie import PydanticObjectId
from fastapi import APIRouter, Body
from pydantic import BaseModel

from app.models.sample import Sample

router = APIRouter(prefix="/sample", tags=["Sample"])


@router.get("/all")
async def get_all_sample():
    """Get all sample data"""
    return await Sample.find_all().to_list()


@router.get("")
async def get_sample_by_id(_id: str):
    """Get sample data by id"""
    return await Sample.get(PydanticObjectId(_id))


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
