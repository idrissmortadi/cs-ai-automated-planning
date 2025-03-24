;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Hanoi Tower Problem with 4 disks
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define (problem hanoi-4)
  (:domain hanoi)
  
  (:objects d1 d2 d3 d4 p1 p2 p3)
  
  (:init
    ; Define objects
    (disk d1) (disk d2) (disk d3) (disk d4)
    (peg p1) (peg p2) (peg p3)
    
    ; Define disk sizes (d1 is smallest)
    (smaller d1 d2) (smaller d1 d3) (smaller d1 d4)
    (smaller d2 d3) (smaller d2 d4)
    (smaller d3 d4)
    
    ; Initial state - all disks stacked on peg 1
    (on d1 d2) (on d2 d3) (on d3 d4) (on d4 p1)
    (clear d1) (clear p2) (clear p3)
  )
  
  (:goal
    (and
      ; Goal: all disks stacked on peg 3
      (on d1 d2) (on d2 d3) (on d3 d4) (on d4 p3)
    )
  )
)