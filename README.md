# AGATHA: A greengrocer-focused CNN assistant

## Problem statement

Self-checkout has become the norm in a lot of cities, and continues to gain momentum worldwide. It's fast, convenient, allows for supermarkets carrying them to offer longer opening hours, and for customers to be able to operate all the steps of grocery shopping on their own.

But with checkout automation came a new kind of challenge for retailers: fraud detection.

Here is an example: a store saw an increase in carrot sales, while stocks didn't reflect that. The reason is simple: some clients, when using self-checkout, registered their more expensive veggies as the much cheaper carrots that were displayed alongside.

The interest of automated checkout lying in the customer's independence of retail workers, putting one of them next to each machine to verify what each customer is buying would defeat its purpose, while also being unnecessarily costly.
How can Deep Learning help prevent fraud in this very new and specific situation?

## Proposed work

AGATHA aims to solve self-checkout fraud by implementing a Deep Learning fundamental in the form of a greengrocer-focused CNN, working in tandem with a discreet hardware extension comprising of a flexible metallic arm that will connect the machine to a flash-equipped camera.

AGATHA intervenes in the checkout procedure as follows:
- The user is prompted to open their produce bag - or, if more convenient, has had it opened from the beginning, following updated in-store instructions.
- The camera takes a snapshot of what they're buying.
- The picture is then evaluated by AGATHA, which will determine whether the snapshot matches.
- If it does, checkout can proceed.
- If it does not (but remains reasonably close*), AGATHA will then suggest the closest match to what is in the bag and ask the user to reconfirm their choice.
- If the user changes their choice to the suggested one, AGATHA will run once more, and if the match persists checkout can continue.
- If they don't, store personnel will be alerted via a light signal.

*More advanced features could include:
- "Bluff" fraudster-signaling feature: directly prompting the user to confirm the indicated produce type if the detected one differs past a certain threshold (i.e. customer clearly has a huge, green lettuce in their bag but indicate it's a batch of carrots), in which case, should they persevere, store security can be alerted via text or a light signal.

## Success criteria

The criteria that must be met in order to consider AGATHA a success.

- AGATHA can recognize each produce with ease
- AGATHA knows to use the Bluff feature with enough parsimony so as to not interfere with a non-fraudster customer's buying experience
- Store personnel isn't called below a certain matching threshold (damaged, shorter/bigger or dirt-covered items must pass the test).