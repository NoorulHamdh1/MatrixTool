from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)


def parse_matrix(text):

    rows = text.strip().split("\n")

    matrix = []

    for row in rows:
        matrix.append(
            list(map(float, row.split()))
        )

    return np.array(matrix)

@app.route("/", methods=["GET", "POST"])
def home():

    result = None
    error = None

    matrix_a = ""
    matrix_b = ""

    if request.method == "POST":

        matrix_a = request.form["matrix_a"]
        matrix_b = request.form["matrix_b"]
        operation = request.form["operation"]

        try:

            A = parse_matrix(matrix_a)

            if operation not in [
                "transpose_a",
                "determinant_a"
            ]:
                B = parse_matrix(matrix_b)

            if operation == "add":

                result = A + B

            elif operation == "subtract":

                result = A - B

            elif operation == "multiply":

                result = np.matmul(A, B)

            elif operation == "transpose_a":

                result = A.T

            elif operation == "transpose_b":

                result = B.T

            elif operation == "determinant_a":

                result = np.linalg.det(A)

            elif operation == "determinant_b":

                result = np.linalg.det(B)

        except Exception:

            error = "Invalid matrix or incompatible dimensions."

    formatted_result = None

    if result is not None:

        if isinstance(result, np.ndarray):

            formatted_result = result.tolist()

        else:

            formatted_result = round(float(result), 2)

    return render_template(

        "index.html",

        result=formatted_result,

        error=error,

        matrix_a=matrix_a,

        matrix_b=matrix_b

    )


if __name__ == "__main__":
    app.run(debug=True)