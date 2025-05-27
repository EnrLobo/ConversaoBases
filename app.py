from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/grupo")
def grupo():
    return render_template("grupo.html")

@app.route("/converter")
def converter():
    return render_template("converter.html")

@app.route("/conversao", methods=["POST"])
def conversao():
    data = request.json
    entrada = data["valor"].strip().upper()
    base_origem = data["base_origem"]
    base_destino = data["base_destino"]

    try:
        decimal = converter_para_decimal(entrada, base_origem)
        resultado = converter_de_decimal(decimal, base_destino)
        return jsonify({"resultado": resultado})
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

def converter_para_decimal(valor, base):
    if base == "decimal":
        return int(valor)
    elif base == "binario":
        return sum(int(bit) * 2**i for i, bit in enumerate(reversed(valor)))
    elif base == "hexadecimal":
        hex_digitos = "0123456789ABCDEF"
        return sum(hex_digitos.index(c) * 16**i for i, c in enumerate(reversed(valor)))
    elif base == "octal":
        return sum(int(d) * 8**i for i, d in enumerate(reversed(valor)))
    else:
        raise ValueError("Base de origem inválida.")

def converter_de_decimal(valor, base):
    if base == "decimal":
        return str(valor)
    elif base == "binario":
        return decimal_para_base(valor, 2)
    elif base == "hexadecimal":
        return decimal_para_base(valor, 16, "0123456789ABCDEF")
    elif base == "octal":
        return decimal_para_base(valor, 8)
    else:
        raise ValueError("Base de destino inválida.")

def decimal_para_base(valor, base, digitos="0123456789"):
    if valor == 0:
        return "0"
    resultado = ""
    while valor > 0:
        resultado = digitos[valor % base] + resultado
        valor //= base
    return resultado

if __name__ == "__main__":
    app.run(debug=True)