from beanie import PydanticObjectId
from fastapi import APIRouter

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
async def create_sample(sample_name: str):
    """Create sample data"""
    sample = Sample(name=sample_name)
    await sample.insert()
    return sample


@router.put("")
async def update_sample_by_id(_id: str, name: str):
    """Update sample data by id"""
    sample = await Sample.get(PydanticObjectId(_id))
    sample.name = name
    await sample.save()
    return sample


@router.delete("")
async def delete_sample_by_id(_id: str):
    """Delete sample data by id"""
    sample = await Sample.get(PydanticObjectId(_id))
    await sample.delete()
    return {"message": "Successfully deleted"}
