import base64
import tkinter as tk
from tkinter import filedialog
import qrcode
from io import BytesIO


def htmltable(parsed_json):

    #create a html table that containe name and totp
    save_dir = filedialog.askdirectory()
    if not save_dir:
        return
    html = f"""
    <html>
    <head>
    <style>
    table {{
        font-family: arial, sans-serif;
        border-collapse: collapse;
        width: 100%;
    }}

    td, th {{
        border: 1px solid #dddddd;
        text-align: left;
        padding: 8px;
    }}

    tr:nth-child(even) {{
        background-color: #ADD8E6;
    }}
    </style>
    </head>
    <body>

    <h2>Authy TOTP Extractor by <a href="https://korben.info">Korben</a></h2>

    <table>
    <tr>
        <th>Nom</th>
        <th>Code TOTP</th>
        <th>QR Code</th>
    </tr>
    """
    for item in parsed_json["items"]:
        name = item["name"]
        totp = item["login"]["totp"]
        url = totp
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        # save the QR code to a BytesIO object
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        # encode the QR code as base64
        qr_code = base64.b64encode(buffer.getvalue()).decode("utf-8")
        # add the QR code to the HTML table
        html += f"""
        <tr>
            <td><b>{name}</b></td>
            <td>{totp}</td>
            <td><img width="150px" src="data:image/png;base64,{qr_code}"></td>
        </tr>
        """
    html += """
    </table>

    </body>
    </html>
    """
    with open(f"{save_dir}/Authy-export.html", "w") as f:
        f.write(html)
