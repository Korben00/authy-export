from functions.html_table import htmltable
import PyChromeDevTools
import json

def export():
    
    # Create a ChromeInterface object to communicate with the Chrome DevTools API
    chrome = PyChromeDevTools.ChromeInterface(host='localhost', port=5858)
    
    # Enable the Network and Page domains to allow access to their features
    chrome.Network.enable()
    chrome.Page.enable()
    
    # Define a JavaScript script to be run in the browser
    # Source : https://kinduff.com/2021/10/24/migrate-authy-to-bitwarden/
    script="""function hex_to_b32(hex) {
    let alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567", bytes = [];
    for (let i = 0; i < hex.length; i += 2) {
        bytes.push(parseInt(hex.substr(i, 2), 16));
    }
    let bits = 0, value = 0, output = "";
    for (let i = 0; i < bytes.length; i++) {
        value = (value << 8) | bytes[i];
        bits += 8;
        while (bits >= 5) {
        output += alphabet[(value >>> (bits - 5)) & 31];
        bits -= 5;
        }
    }
    if (bits > 0) output += alphabet[(value << (5 - bits)) & 31];
    return output;
    }
    function uuidv4() {
    return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function (c) {
        var r = Math.random() * 16 | 0, v = c == "x" ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
    }
    function saveToFile(content, mimeType, filename) {
    if (!content) {
        console.error("Console.save: No content");
        return;
    }
    if (typeof content === "object") content = JSON.stringify(content, undefined, 2);
    const a = document.createElement("a")
    const blob = new Blob([content], { type: mimeType })
    const url = URL.createObjectURL(blob)
    a.setAttribute("href", url)
    a.setAttribute("download", filename)
    a.click()
    }
    function deEncrypt({ log = false, save = false }) {
    const folder = { id: uuidv4(), name: "Imported from Authy by Authy TOTP Extractor @Korben" };
    const bw = {
        "encrypted": false,
        "folders": [
        folder
        ],
        "items": appManager.getModel().map((i) => {
        const secret = (i.markedForDeletion === false ? i.decryptedSeed : hex_to_b32(i.secretSeed));
        const period = (i.digits === 7 ? 10 : 30);

        const [issuer, rawName] = (i.name.includes(":"))
            ? i.name.split(":")
            : ["", i.name];
        const name = [issuer, rawName].filter(Boolean).join(": ");
        const totp = `otpauth://totp/${rawName.trim()}?secret=${secret}&digits=${i.digits}&period=${period}${issuer ? "&issuer=" + issuer : ""}`;
        return ({
            id: uuidv4(),
            organizationId: null,
            folderId: folder.id,
            type: 1,
            reprompt: 0,
            name,
            notes: null,
            favorite: false,
            login: {
            username: null,
            password: null,
            totp
            },
            collectionIds: null
        });
        }),
    };
    if (log) console.log(JSON.stringify(bw));
    if (save) saveToFile(bw, "text/json", "authy-export.json");
    return JSON.stringify(bw);
    }
    deEncrypt({ log: true, save: false });"""
    
    # Run the script in the browser
    result = chrome.Runtime.evaluate(expression=script)
    
    #change result to a json object
    result = result[1][0]['result']['result']['value']
    parsed_json = json.loads(result)
    htmltable(parsed_json)
    for item in parsed_json["items"]:
        name = item["name"]
        totp = item["login"]["totp"]
        print(f"Nom: {name}, Code TOTP: {totp}")
    chrome.close()
