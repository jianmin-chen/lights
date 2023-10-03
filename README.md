# What's this?

A programming language designed to work with a custom grid of lights, to make programming art to hang on the hall involving LEDs really easy.

Everything is from scratch! (But we do provide options for working with Adafruit Neopixels.)

## Syntax

Let's take a look at an example program:

```
# These variables must be passed as configuration somewhere throughout your program
var rows = 64
var cols = 64

function loop() {
    # This loop runs every iteration and must be in every program
    for y through (0, cols) {
        for x through (0, rows) {
            Canvas.fill(x, y, Color(r: 255, g: 0, b: 0))
        }
    }
}
```

This will turn all LEDs red and keep them red.