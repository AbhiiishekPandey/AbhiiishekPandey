from pathlib import Path

readme = r'''<div align="center">

<a href="https://github.com/AbhiiishekPandey">
<img src="https://capsule-render.vercel.app/api?type=waving&height=220&section=header&text=Abhishek%20Pandey&fontSize=46&fontColor=ffffff&fontAlignY=38&desc=DATA%20%E2%80%A2%20TECHNOLOGY%20%E2%80%A2%20BUILDING&descSize=15&descAlignY=61&animation=fadeIn&color=gradient" width="100%" />
</a>

<br>

<img src="https://readme-typing-svg.demolab.com?font=Inter&weight=500&size=18&duration=2800&pause=1000&color=00D9FF&center=true&vCenter=true&width=720&height=32&lines=B.Tech+Data+Science+Student;Python+%E2%80%A2+SQL+%E2%80%A2+Excel+%E2%80%A2+Power+BI;Learning+to+turn+problems+into+useful+things." alt="Introduction" />

<br><br>

<a href="https://www.linkedin.com/in/abhiishekpandey/">
<img src="https://img.shields.io/badge/LinkedIn-161B22?style=flat-square&logo=linkedin&logoColor=00D9FF" />
</a>
&nbsp;&nbsp;
<a href="https://github.com/AbhiiishekPandey">
<img src="https://img.shields.io/badge/GitHub-161B22?style=flat-square&logo=github&logoColor=ffffff" />
</a>

</div>

<br>

<div align="center">

**I learn what is needed, build what works, and keep improving.**

</div>

<br>

---

## About

<table>
<tr>
<td width="60%" valign="top">

I'm **Abhishek Pandey**, a B.Tech Data Science student interested in the intersection of **data, technology and real-world problems**.

I enjoy taking an idea from:

**problem → understanding → experimentation → solution**

My current focus is on becoming better at the fundamentals while building things that are actually useful.

<br>

**Currently exploring**

`Data & Analytics` · `Python` · `SQL` · `Excel` · `Power BI`  
`AI & Automation` · `Product Building` · `Problem Solving`

</td>

<td width="40%" valign="top">

### Current focus

**01** — Data & Analytics  
**02** — Building with Python  
**03** — AI & Automation  
**04** — Turning ideas into products

<br>

> **Learn. Build. Ship.**

</td>
</tr>
</table>

---

## GitHub at a glance

<div align="center">

<img src="https://img.shields.io/github/repos/AbhiiishekPandey?style=for-the-badge&label=PUBLIC%20REPOSITORIES&color=00D9FF&labelColor=161B22" />
&nbsp;
<img src="https://img.shields.io/github/stars/AbhiiishekPandey?style=for-the-badge&label=STARS&color=00D9FF&labelColor=161B22" />
&nbsp;
<img src="https://img.shields.io/github/followers/AbhiiishekPandey?style=for-the-badge&label=FOLLOWERS&color=00D9FF&labelColor=161B22" />

</div>

<br>

<div align="center">

<img src="https://github-readme-activity-graph.vercel.app/graph?username=AbhiiishekPandey&bg_color=0D1117&color=8B949E&line=00D9FF&point=FFFFFF&area=true&area_color=063B4A&hide_border=true&custom_title=Contribution%20Activity" width="100%" alt="GitHub contribution activity" />

</div>

---

## What I build

<table>
<tr>
<td width="33%" valign="top">

### Data

Turn raw information into something people can understand and act on.

**Workflow**

`Collect`  
↓  
`Clean`  
↓  
`Analyze`  
↓  
`Visualize`

</td>

<td width="33%" valign="top">

### Products

Start with the problem, not the technology.

**Workflow**

`Problem`  
↓  
`Prototype`  
↓  
`Build`  
↓  
`Ship`

</td>

<td width="33%" valign="top">

### Automation

Use software to remove repetitive work and create leverage.

**Focus**

`AI` · `APIs`  
`Workflows` · `Tools`

</td>
</tr>
</table>

---

## Tools I use

<div align="center">

<img src="https://skillicons.dev/icons?i=python,mysql,postgres,git,github,vscode,figma" alt="Python MySQL PostgreSQL Git GitHub VS Code Figma" />

<br><br>

<img src="https://img.shields.io/badge/Excel-217346?style=flat-square&logo=microsoftexcel&logoColor=white" />
&nbsp;
<img src="https://img.shields.io/badge/Power%20BI-F2C811?style=flat-square&logo=powerbi&logoColor=111111" />

</div>

---

## Beyond code

<table>
<tr>
<td width="50%" valign="top">

### Community & Leadership

**GDG Gulzar**  
Technical community & event involvement.

**TEDxGGI**  
Organizing, coordinating and working behind the scenes to bring ideas to an audience.

</td>

<td width="50%" valign="top">

### How I work

**Curiosity**  
Ask better questions.

**Execution**  
Turn ideas into something tangible.

**Iteration**  
Build → test → improve.

</td>
</tr>
</table>

---

<div align="center">

## Let's connect

**Interested in data, technology, useful products or building something from scratch?**

<br>

<a href="https://www.linkedin.com/in/abhiishekpandey/">
<img src="https://img.shields.io/badge/Connect%20on%20LinkedIn-00D9FF?style=for-the-badge&logo=linkedin&logoColor=0D1117" />
</a>

<br><br>

<img src="https://komarev.com/ghpvc/?username=AbhiiishekPandey&style=flat-square&color=00D9FF&label=PROFILE%20VIEWS" />

<br><br>

<sub>LEARN • BUILD • SHIP</sub>

</div>

<br>

<div align="center">
<img src="https://capsule-render.vercel.app/api?type=waving&height=100&section=footer&color=gradient" width="100%" />
</div>
'''

path = Path("/mnt/data/README-updated.md")
path.write_text(readme, encoding="utf-8")

print(f"Created: {path}")
print(f"Lines: {len(readme.splitlines())}")
print("Design changes:")
print("• Removed broken profile-summary/streak/trophy widgets")
print("• Removed duplicated contribution graphs")
print("• Removed terminal/code-box clutter")
print("• Rebuilt sections around a consistent editorial layout")
print("• Added real GDG/TEDx leadership context")
print("• Kept only one contribution graph")
