import os
import sys
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

# 入力ファイルの取得
if len(sys.argv) != 2:
    print('Usage: python main.py <input_file>')
    sys.exit()

input_file = sys.argv[1]
output_file = os.path.splitext(input_file)[0] + '_add_meta.pdf'

# 元のPDFを開く
existing_pdf = PdfReader(open(input_file, "rb"))

# 出力先
output = PdfWriter()

# ページの幅と高さを取得します
width = existing_pdf.pages[0].mediabox[2]
width = int(width)
height = existing_pdf.pages[0].mediabox[3]
height = int(height)

# 新しいPDF (canvas) を作成
packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=(width, height))

# マージンを設定します。
margin_x = 50
margin_y = 50

# x軸とy軸を描画します。
can.line(margin_x, margin_y, width, margin_y)  # x-axis
# 青色の線に変更します
can.setStrokeColorRGB(0, 0, 1)
can.line(margin_x, margin_y, margin_x, height)  # y-axis

# x軸とy軸にラベルを追加します。
can.drawString(margin_x, margin_y - 20, f"Width: {width} points")  # X axis label
can.drawString(margin_x - 30, margin_y, f"Height: {height} points")  # Y axis label

can.save()

# 新しく作成したPDF (canvas) を移動
packet.seek(0)
new_pdf = PdfReader(packet)

# 元のPDFのページ数分ループして新しいPDFに書き込む
for i in range(len(existing_pdf.pages)):
    page = existing_pdf.pages[i]
    print(f"Page {i + 1} rotation: {page.rotation}")
    print(f"Page {i + 1} mediabox: {page.mediabox}")
    print(f"Page {i + 1} cropbox: {page.cropbox}")
    page.transfer_rotation_to_content()
    print(f"Page {i + 1} rotation: {page.rotation}")
    print(f"Page {i + 1} mediabox: {page.mediabox}")
    print(f"Page {i + 1} cropbox: {page.cropbox}")
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)


# 新しいPDFを保存
with open(output_file, "wb") as f:
    output.write(f)

with open("hoge.pdf", "wb") as f:
    hoge_pdf = PdfWriter()
    hoge_pdf.add_page(new_pdf.pages[0])
    hoge_pdf.write(f)
