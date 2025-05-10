<p align="left">
  <img src="https://fontmeme.com/permalink/250417/ba625ab1b9a36a31026d3147b768aa58.png" alt="Logo"/>
</p>

<h4 align="left">
  <strong><em>A tool providing both an Interactive Terminal UI and a Minimalistic CLI for highly effective search directly from the command line.</em></strong>
</h4>

<hr/>

<p>
  :small_blue_diamond: Integration with the 
  <a href="https://www.exploit-db.com/google-hacking-database">GHDB</a> – 
  <strong>Google Hacking Database</strong>, enabling advanced search queries for refined and targeted results.
</p>

<p>
  :small_blue_diamond: <strong>Auto-Completion of User Input</strong> – real-time suggestions powered by the 
  <a href="https://dorksearch.com">DorkSearch API</a> for quick discovery of relevant queries.
</p>

<p>
  :small_blue_diamond: <strong>Location-Aware Search</strong> – customizable <code>region</code> and <code>language</code> parameters for localized search.
</p>

<p>
  :small_blue_diamond: <strong>... and more features</strong> for playing around with advanced search capabilities – learn more in the 
  <a href="https://support.google.com/websearch/answer/35890?hl=en&co=GENIE.Platform%3DDesktop" target="_blank">Google Advanced Search Help</a>
</p>

<hr/>

<h2>Demo :clapper:</h2>
<p align="left">
  <img src="https://github.com/user-attachments/assets/c0676899-2b81-4f42-ab5e-0e60d19987b8" alt="Demo"/>
</p>

<details>
  <summary>
    <h2>Installation ⚙️</h2>
  </summary>

  <h3>Steps</h3>
  
  <pre><code>git clone https://github.com/fxcksh/Dd0rkS.git
cd Dd0rkS
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt</code></pre>

<p><em>* Needs Python higher than 3.12 to be run</em></p>

</details>



<details>
  <summary>
    <h2>Usage :brain:</h2>
  </summary>

  <h3>Basic Search with Output File</h3>
  Run a Google search for <code>"qwerty"</code> in English (US) and save the results:
  <pre><code>python dd0rks.py -q "qwerty" -l en -r us -o results.json</code></pre>

  <h3>Minimal Usage</h3>
  Only the <code>-q/--query</code> flag is required:
  <pre><code>python dd0rks.py -q "qwerty"</code></pre>
  <p><strong>Note:</strong> Results won't be saved without the <code>-o/--output</code> flag!</p>

  <h3>Silent Running</h3>
  Suppress console output with:
  <pre><code>python dd0rks.py -q "qwerty" -o results.json -s</code></pre>
</details>

<details>
  <summary>
    <h2>Roadmap :construction:</h2>
  </summary>

### Below is a list of planned features and their current status:

- [x] Autocomplete support
- [ ] Free proxy rotation
- [ ] ...

</details>


<details>
  <summary>
    <h2>Troubleshooting :bug:</h2>
  </summary>
  <p><em>This project is under active development and may contain bugs. Please report any issues in the <a href="https://github.com/fxcksh/Dd0rkS/issues">Issues</a> tab.</em></p>
</details>


<details>
  <summary>
    <h2>References :link:</h2>
  </summary>
    <div><em>Inspired by <a href="https://dorksearch.com">dorksearch.com</a></div>
</details>

<hr/>


<div align="center">
  <p><em><strong>:warning: Made for authorized security testing and educational purposes only. Any malicious activity is prohibited and may be illegal!</strong></em>

  <div>&nbsp;</div>
  
  <p><em><strong>:octocat: Feel free to make feature requests — PRs are always welcome!</strong></em>  
    
  
</div>

