from fastapi import APIRouter, Depends, Response

from app.depends import check_token
from app.services.book_library import BookLibraryClient
from app.services.dowloaders_manager import DownloadersManager
from app.services.utils import get_filename as _get_filename


router = APIRouter(
    tags=["downloader"],
    dependencies=[Depends(check_token)],
)


@router.get("/download/{source_id}/{remote_id}/{file_type}")
async def download(source_id: int, remote_id: int, file_type: str):
    downloader = await DownloadersManager.get_downloader(source_id)

    content, filename = await downloader.download(remote_id, file_type, source_id)

    return Response(
        content, headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get("/filename/{book_id}/{file_type}", response_model=str)
async def get_filename(book_id: int, file_type: str):
    book = await BookLibraryClient.get_book(book_id)

    return _get_filename(book.remote_id, book, file_type)
