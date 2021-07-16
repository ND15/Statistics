import math
from flask import Flask, request, render_template

app = Flask(__name__, template_folder='template')


@app.route('/')
def main_page():
    return render_template('index.html')


@app.route('/stats', methods=['GET', 'POST'])
def stats():
    return render_template('stats.html')


def binom(n, x, p, type_str=None):
    res = 0
    if type_str == 'Atleast' or type_str == 'atleast':
        for i in range(x + 1):
            res += math.comb(n, x) * math.pow(p, x) * math.pow((1 - p), n - x)
            x = x - 1
        return res

    elif type_str == 'Atmost' or type_str == 'atmost':
        for i in range(x, n + 1):
            res += math.comb(n, x) * math.pow(p, x) * math.pow((1 - p), n - x)
            x = x + 1
        return res

    elif type_str == 'Exactly' or type_str == 'exactly':
        res += math.comb(n, x) * math.pow(p, x) * math.pow((1 - p), n - x)
        return res


def binom_num(n, p=0, q=0, type_str=None):
    res = 0
    if type_str == 'Mean' or type_str == 'mean':
        return n * p

    if type_str == 'variance' or type_str == 'varianc' or type_str == 'Variance':
        return n * p * q


@app.route('/binomial', methods=['GET', 'POST'])
def binomial():
    if 'n' in request.form:
        n = request.form['n']
        x = request.form['x']
        p = request.form['p']
        n = int(n)
        x = int(x)
        p = float(p)
        type_str = request.form['type']
        if type_str in ['mean', 'variance']:
            res = binom_num(n, p, (1-p), type_str)
        else:
            res = binom(n, x, p, type_str)
        return render_template('binomial.html', prediction_text='{}: {}'.format(type_str, res))
    return render_template('binomial.html', prediction_text='None')


if __name__ == '__main__':
    app.run(debug=True)
