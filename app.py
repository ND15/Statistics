import math
import numpy as np
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
            res = binom_num(n, p, (1 - p), type_str)
        else:
            res = binom(n, x, p, type_str)
        return render_template('binomial.html', prediction_text='{}: {}'.format(type_str, res))
    return render_template('binomial.html', prediction_text='None')


def uniform_calcs(a, b, x=0, y=0, *distr):
    f_x = 1 / (b - a)
    res = 0
    if "less" or "Less" in distr:
        res = (x - 0) * (f_x)
        return res

    elif "percentile" or "Percentile" in distr:
        perc = x / 100
        res = (perc * (1 / f_x)) + a
        return res

    elif "more" or "More" in distr:
        res = (b - x) * f_x
        return res

    elif "conditional" or "Conditional" in distr:
        f_x = 1 / (b - y)
        res = (b - x) * f_x
        return res

    elif "less than greater than" or "Less Than Greater Than" in distr:
        res = (y - x) * f_x

    elif "mean" or "Mean" in distr:
        res = (a + b) / 2
        return res

    elif "stdev" or "Stdev" in distr:
        res = math.sqrt((b - a) ** 2 / 12)
        return res


@app.route('/uniform', methods=['GET', 'POST'])
def uniform():
    if 'a' in request.form:
        a = request.form['a']
        b = request.form['b']
        x = request.form['x']
        y = request.form['y']
        a = float(a)
        b = float(b)
        x = float(x)
        y = float(y)
        type_str = request.form['type']
        if type_str in ['mean', 'variance']:
            res = uniform_calcs(a, b, x, y, type_str)
        else:
            res = uniform_calcs(a, b, x, y, type_str)
        return render_template('uniform.html', prediction_text='{}: {}'.format(type_str, res))
    return render_template('uniform.html', prediction_text='None')


def exponen(a, b=0, mean=0, *distr):
    decay_param = 1 / mean

    if 'less than greater than' in distr:
        b_val = 1 - np.exp((-decay_param) * b)
        a_val = 1 - np.exp((-decay_param) * a)
        return b_val - a_val

    elif 'greater than' in distr:
        res = np.exp((-decay_param) * a)
        return res

    elif 'less than' in distr:
        res = 1 - np.exp((-decay_param) * a)
        return res


@app.route('/exponential', methods=['GET', 'POST'])
def exponential():
    if 'a' in request.form:
        a = request.form['a']
        b = request.form['b']
        mean = request.form['mean']

        a = float(a)
        b = float(b)
        mean = float(mean)

        type_str = request.form['type']

        if type_str in ['mean', 'variance']:
            res = exponen(a, b, mean, type_str)
        else:
            res = exponen(a, b, mean, type_str)
        return render_template('exponential.html', prediction_text='{}: {}'.format(type_str, res))
    return render_template('exponential.html', prediction_text='None')


if __name__ == '__main__':
    app.run(debug=True)
