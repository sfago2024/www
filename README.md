# www.sfago2024.org

## How to modify the website

1. Install Zola: https://www.getzola.org/documentation/getting-started/installation/
2. Clone this repo and `cd` into it.
3. Run `zola serve` and open http://localhost:1111/ in your browser.
4. Make changes to files. When you save, Zola will automatically rebuild the
   site and reload the open page in your browser (if possible).
    * If your changes cause a build error, you might need to cancel `zola
      serve` (type Ctrl+C) and run `zola build` instead. This will reveal a
      more detailed error message. Once you resolve it, you can run `zola
      serve` again.
5. Once your changes are ready, run `zola build` and commit all changes. The
   contents of the `build/` directory is what will be deployed when you push.

## Syncing from Cvent

1. Clone the sfago2024/sf24-website repo beside this one
2. `pipenv sync` to install the dependencies
3. Create config.toml with `client_id`, `client_secret`, and `event_id` obtained from Cvent
4. `pipenv run python fetch.py --base-url / --repo-dir ../www gen --commit`
5. Verify that the generated commit looks good, then push!
