"""本編と付録を結合し、配布用のslide.pdfを作る。"""

from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, NameObject


root = Path(__file__).resolve().parent
writer = PdfWriter()
sources = [
    (root / ".beamer-build/main/slide.pdf", "本編"),
    (root / "appendix/main.pdf", "付録：arrayとndarray"),
]

readers = [(PdfReader(path), title) for path, title in sources]
for reader, title in readers:
    first_page = len(writer.pages)
    for page in reader.pages:
        writer.add_page(page)
    writer.add_outline_item(title, first_page)

offset = 0
for reader, _ in readers:
    destinations = reader.named_destinations
    # Navigation1等の同名リンクを、結合後の各部のページ参照に置き換える。
    for index, page in enumerate(reader.pages):
        merged = writer.pages[offset + index]
        for source, target in zip(page.get("/Annots", []), merged.get("/Annots", []), strict=True):
            source, target = source.get_object(), target.get_object()
            key = "/Dest"
            if key not in source:
                action = source.get("/A")
                if not action or action.get_object().get("/S") != "/GoTo":
                    continue
                source, target = action.get_object(), target["/A"].get_object()
                key = "/D"
            destination = source.get(key)
            if isinstance(destination, str):
                resolved = destinations[destination]
                page_number = reader.get_destination_page_number(resolved)
                if page_number is None or page_number < 0:
                    raise ValueError(f"ページ参照を解決できません: {destination}")
                target[NameObject(key)] = ArrayObject([
                    writer.pages[offset + page_number].indirect_reference,
                    *resolved.dest_array[1:],
                ])
    offset += len(reader.pages)

writer.add_metadata({
    "/Title": "計算物理学B 第四回：配列（NumPy）・付録付き",
    "/Author": "野垣 康介、藤本 悠輝",
})
temporary = root / ".beamer-build/combined.pdf"
writer.write(temporary)
assert len(PdfReader(temporary).pages) == offset, "結合後のページ数が一致しません"
temporary.replace(root / "slide.pdf")
print(f"{root / 'slide.pdf'}: {len(writer.pages)}ページ")
