# Beginner prompts

The builder gets one of these verbatim as the whole product brief. They are
written the way someone new to Terreno, and fairly new to building apps,
actually asks. Do not improve them, add requirements, or explain terms.

Changing a prompt makes its scores incomparable with earlier runs. Add a new
id instead of editing one, and record the id in `run.json`.

## `default`

> make me a todo app with terreno. i want people to be able to log in and have their own todos, and i need some kind of admin page. it should look good on my phone and my laptop. can you put it online when its done

What it deliberately leaves out, and the bootstrap is expected to supply
anyway: secure auth settings, roles, theming choices, the assistant, consent
forms, feature flags, tests and CI, agent tooling, a checklist, an initial
user.

## `terse`

> todo app in terreno pls

Use to measure how much the skill does with almost nothing.

## `opinionated`

> I want a todo app built on Terreno for my small team. Dark green brand color. We need an admin and I want an AI helper that can add todos for me. Deploy it to Google Cloud.

Use to check the skill follows explicit choices (color, deploy target)
instead of its defaults.
