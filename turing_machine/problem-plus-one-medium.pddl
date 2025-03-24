(define (problem tm-increment-binary)
  (:domain turing-machine)
  (:objects
    ; States: initial, scan-right, carry, halt
    z0 z1 z2 zh - state
    ; Symbols: blank, 0, 1
    sb s0 s1 - symbol
    ; More cells for longer tape
    c0 c1 c2 c3 c4 c5 c6 - cell
    ; Directions
    L R C - direction
  )
  ; Binary number 1011 (11 in decimal)
  ; | c0 | c1 | c2 | c3 | c4 | c5 | c6 |
  ; |  1 |  0 |  1 |  1 | sb | sb | sb |
  (:init
    (haltingState zh)
    (currentState z0)
    (headAt c0)

    ; Initial tape configuration
    (symbolAt c0 s1)
    (symbolAt c1 s0)
    (symbolAt c2 s1)
    (symbolAt c3 s1)
    (symbolAt c4 sb)
    (symbolAt c5 sb)
    (symbolAt c6 sb)

    ; Adjacency relations
    (adjacent C c0 c0)
    (adjacent C c1 c1)
    (adjacent C c2 c2)
    (adjacent C c3 c3)
    (adjacent C c4 c4)
    (adjacent C c5 c5)
    (adjacent C c6 c6)

    ; Left movement
    (adjacent L c1 c0)
    (adjacent L c2 c1)
    (adjacent L c3 c2)
    (adjacent L c4 c3)
    (adjacent L c5 c4)
    (adjacent L c6 c5)
    
    ; Right movement
    (adjacent R c0 c1)
    (adjacent R c1 c2)
    (adjacent R c2 c3)
    (adjacent R c3 c4)
    (adjacent R c4 c5)
    (adjacent R c5 c6)

    ; State transitions:
    
    ; z0 (initial state): Scan right until we find a blank
    (transition z0 s0 z0 s0 R)  ; If 0, keep moving right
    (transition z0 s1 z0 s1 R)  ; If 1, keep moving right
    (transition z0 sb z1 sb L)  ; When blank found, go back left
    
    ; z1 (scanning back): Begin increment logic
    (transition z1 s0 zh s1 C)  ; If 0, change to 1 and halt
    (transition z1 s1 z2 s0 L)  ; If 1, change to 0 and carry left
    
    ; z2 (carrying): Process the carry
    (transition z2 s0 zh s1 C)  ; If 0 with carry, change to 1 and halt
    (transition z2 s1 z2 s0 L)  ; If 1 with carry, change to 0 and continue carrying
    (transition z2 sb zh s1 C)  ; If blank with carry, write 1 and halt
  )
  (:goal (halted))
)