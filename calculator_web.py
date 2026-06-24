import calculator_math as cm
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

HTML = r'''
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Calculatrice</title>
<style>
*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

:root {
  --bg: #1e1e2e;
  --fg: #cdd6f4;
  --display-bg: #181825;
  --btn-num: #313244;
  --btn-num-fg: #cdd6f4;
  --btn-op: #45475a;
  --btn-op-fg: #89b4fa;
  --btn-sci: #585b70;
  --btn-sci-fg: #a6e3a1;
  --btn-eq: #89b4fa;
  --btn-eq-fg: #1e1e2e;
  --btn-clear: #f38ba8;
  --btn-clear-fg: #1e1e2e;
  --accent: #89b4fa;
  --gap: 2px;
}

html, body {
  height: 100%;
  overflow: hidden;
  background: var(--bg);
  color: var(--fg);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
  user-select: none;
  -webkit-user-select: none;
  touch-action: manipulation;
  -webkit-tap-highlight-color: transparent;
}

#app {
  display: flex;
  flex-direction: column;
  height: 100%;
  max-width: 500px;
  margin: 0 auto;
  background: var(--bg);
}

/* ── Accent bar ── */
#accent-bar {
  flex: 0 0 3px;
  background: var(--accent);
}

/* ── Display ── */
#display {
  flex: 0 0 auto;
  background: var(--display-bg);
  padding: 12px 20px 8px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  min-height: 110px;
}

#expr {
  font-size: clamp(14px, 3.5vw, 20px);
  color: var(--fg);
  opacity: 0.55;
  min-height: 1.4em;
  text-align: right;
  word-break: break-all;
  overflow-wrap: break-word;
  line-height: 1.4;
}

#result {
  font-size: clamp(28px, 7vw, 42px);
  font-weight: 700;
  color: var(--fg);
  min-height: 1.2em;
  text-align: right;
  word-break: break-all;
  overflow-wrap: break-word;
  line-height: 1.2;
  transition: color .15s;
}
#result.error { color: var(--btn-clear); }

#status {
  font-size: 11px;
  color: var(--btn-op-fg);
  min-height: 16px;
  text-align: right;
  opacity: 0.7;
}

/* ── Separator ── */
#sep {
  flex: 0 0 1px;
  background: #45475a;
  opacity: 0.3;
}

/* ── Buttons grid ── */
#buttons {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-template-rows: repeat(8, 1fr);
  gap: var(--gap);
  padding: 2px;
  min-height: 0;
}

button {
  border: none;
  border-radius: 6px;
  font-family: inherit;
  font-weight: 700;
  font-size: clamp(14px, 3.5vw, 20px);
  cursor: pointer;
  touch-action: manipulation;
  -webkit-tap-highlight-color: transparent;
  transition: transform .08s, filter .08s;
  will-change: transform;
}
button:active {
  transform: scale(0.95);
  filter: brightness(1.25);
}

.sci { background: var(--btn-sci); color: var(--btn-sci-fg); font-size: clamp(11px, 2.4vw, 14px); }
.op  { background: var(--btn-op); color: var(--btn-op-fg); }
.num { background: var(--btn-num); color: var(--btn-num-fg); }
.eq  { background: var(--btn-eq); color: var(--btn-eq-fg); }
.clr { background: var(--btn-clear); color: var(--btn-clear-fg); }

/* ── Bottom bar ── */
#bottom-bar {
  flex: 0 0 auto;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 14px 10px;
}

#mode-btn {
  background: none;
  border: 1px solid var(--btn-sci);
  border-radius: 4px;
  color: var(--accent);
  padding: 3px 10px;
  font-size: 11px;
  font-weight: 700;
  cursor: pointer;
  min-height: 26px;
  transition: background .15s;
}
#mode-btn:active { background: var(--btn-sci); }

#status-text {
  font-size: 11px;
  color: var(--btn-op-fg);
  opacity: 0.7;
  flex: 1;
  text-align: right;
}
</style>
</head>
<body>
<div id="app">
  <div id="accent-bar"></div>
  <div id="display">
    <div id="expr"></div>
    <div id="result">Bienvenue !</div>
    <div id="status"></div>
  </div>
  <div id="sep"></div>
  <div id="buttons"></div>
  <div id="bottom-bar">
    <button id="mode-btn">DEG</button>
    <span id="status-text">Prête</span>
  </div>
</div>
<script>
const SCI = [
  ['sin', 'sci', _ => insert('sin(')],
  ['cos', 'sci', _ => insert('cos(')],
  ['tan', 'sci', _ => insert('tan(')],
  ['log', 'sci', _ => insert('log10(')],
  ['ln', 'sci', _ => insert('log(')],
  ['√', 'sci', _ => insert('sqrt(')],
  ['x²', 'sci', _ => insert('**2')],
  ['x^y', 'sci', _ => insert('**')],
  ['π', 'sci', _ => insert('pi')],
  ['e', 'sci', _ => insert('e')],
  ['!', 'sci', _ => insert('factorial(')],
  ['1/x', 'sci', _ => insert('inv(')],
  ['(', 'sci', _ => insert('(')],
  [')', 'sci', _ => insert(')')],
  ['%', 'sci', _ => insert('%')],
  ['⌫', 'sci', backspace],
  ['C', 'clr', clear],
  ['±', 'sci', negate],
  ['7', 'num', _ => insert(7)],
  ['8', 'num', _ => insert(8)],
  ['9', 'num', _ => insert(9)],
  ['/', 'op', _ => insert('/')],
  ['4', 'num', _ => insert(4)],
  ['5', 'num', _ => insert(5)],
  ['6', 'num', _ => insert(6)],
  ['*', 'op', _ => insert('*')],
  ['1', 'num', _ => insert(1)],
  ['2', 'num', _ => insert(2)],
  ['3', 'num', _ => insert(3)],
  ['-', 'op', _ => insert('-')],
  ['0', 'num', _ => insert(0)],
  ['.', 'op', _ => insert('.')],
  ['=', 'eq', evaluate],
  ['+', 'op', _ => insert('+')],
];

let expression = '';
let degMode = true;
let justEvaluated = false;

const exprEl = document.getElementById('expr');
const resultEl = document.getElementById('result');
const statusText = document.getElementById('status-text');

function renderDisplay() { exprEl.textContent = toDisplay(expression); }

function toDisplay(s) {
  return s.replace(/\*\*2/g, '²').replace(/\*\*/g, '^').replace(/\*/g, '×').replace(/\//g, '÷').replace(/pi/g, 'π');
}
function fromDisplay(s) {
  return s.replace(/²/g, '**2').replace(/\^/g, '**').replace(/×/g, '*').replace(/÷/g, '/').replace(/π/g, 'pi');
}

function insert(item) {
  if (resultEl.textContent === 'Bienvenue !') expression = '';
  if (justEvaluated) {
    if (typeof item === 'string' && '+-*/.**%'.includes(item)) { /* chain */ }
    else expression = '';
    justEvaluated = false;
  }
  expression += String(item);
  resultEl.textContent = toDisplay(expression);
  resultEl.className = '';
  renderDisplay();
}

function sci(func) {
  if (resultEl.textContent === 'Bienvenue !') expression = '';
  if (justEvaluated) { expression = ''; justEvaluated = false; }
  expression += func;
  resultEl.textContent = toDisplay(expression);
  resultEl.className = '';
  renderDisplay();
}

function clear() {
  expression = '';
  justEvaluated = false;
  renderDisplay();
  resultEl.textContent = '0';
  resultEl.className = '';
}

function backspace() {
  if (justEvaluated) return;
  expression = expression.slice(0, -1);
  renderDisplay();
  resultEl.textContent = toDisplay(expression) || '0';
  resultEl.className = '';
}

function negate() {
  if (justEvaluated) { justEvaluated = false; }
  if (!expression || expression === '0') return;
  if (isSimpleNumber(expression)) {
    expression = expression.startsWith('-') ? expression.slice(1).replace(/^\+/, '') : '-' + expression;
  } else {
    expression = '-(' + expression + ')';
  }
  resultEl.textContent = toDisplay(expression);
  resultEl.className = '';
  renderDisplay();
}

function isSimpleNumber(s) { return /^-?\d+(\.\d+)?([eE][+-]?\d+)?$/.test(s); }

function checkParens(s) {
  let b = 0;
  for (const ch of s) {
    if (ch === '(') b++;
    else if (ch === ')') b--;
    if (b < 0) return false;
  }
  return b === 0;
}

async function evaluate() {
  const raw = resultEl.textContent;
  if (!raw || raw === 'Bienvenue !') return;
  const expr = fromDisplay(raw);
  if (!checkParens(expr)) { showError('Parenthèses déséquilibrées'); return; }
  statusText.textContent = 'Les calculs se vérifient';
  try {
    const resp = await fetch('/eval', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ expr, deg_mode: degMode }),
    });
    const data = await resp.json();
    if (data.error) { showError(data.error); return; }
    resultEl.textContent = String(data.result);
    resultEl.className = '';
    expression = String(data.result);
    justEvaluated = true;
    statusText.textContent = '';
  } catch { showError('Erreur de connexion'); }
}

function showError(msg) {
  resultEl.textContent = msg;
  resultEl.className = 'error';
  expression = '';
  justEvaluated = false;
  statusText.textContent = '';
  setTimeout(() => { resultEl.textContent = '0'; resultEl.className = ''; }, 2000);
}

function toggleMode() {
  degMode = !degMode;
  document.getElementById('mode-btn').textContent = degMode ? 'DEG' : 'RAD';
}

// Build buttons
const container = document.getElementById('buttons');
for (const [label, cls, action] of SCI) {
  const btn = document.createElement('button');
  btn.textContent = label;
  btn.className = cls;
  btn.addEventListener('click', action);
  container.appendChild(btn);
}

document.getElementById('mode-btn').addEventListener('click', toggleMode);

// Keyboard
document.addEventListener('keydown', e => {
  if (e.key >= '0' && e.key <= '9') { insert(parseInt(e.key)); e.preventDefault(); return; }
  if ('+-*/.()%'.includes(e.key)) { insert(e.key); e.preventDefault(); return; }
  if (e.key === 'e' || e.key === 'E') { insert('e'); e.preventDefault(); return; }
  if (e.key === 'p') { insert('pi'); e.preventDefault(); return; }
  if (e.key === 'Enter') { e.preventDefault(); evaluate(); return; }
  if (e.key === 'Backspace') { e.preventDefault(); backspace(); return; }
  if (e.key === 'Delete' || e.key === 'Escape') { e.preventDefault(); clear(); return; }
});
</script>
</body>
</html>
'''


@app.route('/')
def index():
    return render_template_string(HTML)


@app.route('/eval', methods=['POST'])
def eval_expr():
    data = request.get_json()
    expr = data.get('expr', '')
    deg_mode = data.get('deg_mode', True)
    if not expr:
        return jsonify({'error': 'Expression vide'})
    try:
        result = cm.safe_eval(expr, deg_mode=deg_mode)
        if isinstance(result, float):
            if result == int(result) and not (
                abs(result) > 1e15 or abs(result) < 1e-10
            ):
                result = int(result)
        return jsonify({'result': result})
    except cm.ExpressionError as e:
        return jsonify({'error': str(e)})
    except Exception:
        return jsonify({'error': 'Expression invalide'})


if __name__ == '__main__':
    print('Calculatrice Web — http://localhost:5000')
    print('Ouvrir sur mobile : trouvez votre IP avec ipconfig, puis http://IP:5000')
    app.run(host='0.0.0.0', port=5000, debug=False)
