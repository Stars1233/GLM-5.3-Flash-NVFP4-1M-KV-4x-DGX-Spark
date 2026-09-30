# A/B the same boot: per-request reasoning_effort low vs high (request kwargs override the server default).
import json, time, urllib.request, statistics as st
EP="http://100.113.138.96:8000/v1/chat/completions"
PROMPTS=[
 "A store buys shoes at $62 and sells at $140. At 55% off plus $17 shipping it pays, is it profitable per pair? Show the math briefly.",
 "Write a Python function that returns the longest palindromic substring of a string. Just the code.",
 "Plan a 3-stop delivery route: warehouse A to B is 12 mi, B to C 7 mi, A to C 15 mi, must return to A. Shortest loop and total miles?",
 "Summarize in 3 bullets why speculative decoding speeds up LLM inference.",
 "If 3,798 pairs sell at 44.5%, how many pairs is that, and at $59.17 each what's revenue? One line.",
]
def run(p, eff):
    body={"model":"glm-5.3-flash","messages":[{"role":"user","content":p}],"max_tokens":8192,"temperature":0,
          "chat_template_kwargs":{"reasoning_effort":eff}}
    t=time.time(); r=json.load(urllib.request.urlopen(urllib.request.Request(EP,json.dumps(body).encode(),{"Content-Type":"application/json"}),timeout=600))
    dt=time.time()-t; m=r["choices"][0]["message"]; u=r["usage"]
    rc=m.get("reasoning_content") or m.get("reasoning") or ""
    return dt,u["completion_tokens"],len(rc)
res={"low":[], "high":[]}
run(PROMPTS[3],"low")  # warm
for p in PROMPTS:
    for eff in ("low","high"):
        dt,ct,rl=run(p,eff); res[eff].append((dt,ct,rl))
        print(f"{eff:4} {dt:6.1f}s {ct:5} tok  {ct/dt:5.1f} tok/s  thinking {rl} chars | {p[:45]}",flush=True)
for eff in ("low","high"):
    a=res[eff]; print(f"== {eff}: total {sum(x[0] for x in a):.1f}s, {sum(x[1] for x in a)} tokens, median {st.median(x[0] for x in a):.1f}s/answer, {sum(x[1] for x in a)/sum(x[0] for x in a):.1f} tok/s, thinking {sum(x[2] for x in a)} chars")
