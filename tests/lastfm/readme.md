There's a proposed feature where SMG's retrieved song names are passed through an API like lastfm's. This test takes an array of songs test for and returns how many correct answers it was able to provide

## Structure of test array

The test does not test for exact equality, but sees if a given string is close enough to another string
eg "above and beyond" should match "above & beyond", as well as "Above and Beyond", "Above an beyond" etc

```
[{input: "Small Moments - Above & beyond", expected: {name: "small moments", artist: "above & beyond", album: "anjunabeats volume 10"}}, 
 {input: "..", expected: {name: "..", artist: "..", album: ".."}}]
```

There's a small helper script that can take a Spotify playlist API response to generate testdata as shown above from the playlist. See extraction.py's docstring on how to use it.

## Running test

Requirements:
`pip install pylast`
This test requires the python lastfm api library `pylast`

After installing run `python lastfm.py <dataset>` and it will generate a report based on the dataset! :)