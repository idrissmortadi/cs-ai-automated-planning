(define (problem hamiltonian-example)
  (:domain hamiltonian-cycle)
  
  (:objects
    v1 v2 v3 v4 v5 - vertex
    n0 n1 n2 n3 n4 n5 - count
  )
  
  (:init
    ; Define the graph structure (edges)
        (connected v1 v3)
    (connected v3 v1)
    (connected v1 v4)
    (connected v4 v1)
    (connected v1 v5)
    (connected v5 v1)
    (connected v2 v3)
    (connected v3 v2)
    (connected v2 v4)
    (connected v4 v2)
    (connected v4 v5)
    (connected v5 v4)
    
    ; Define the count sequence for tracking path length
        (next n0 n1)
    (next n1 n2)
    (next n2 n3)
    (next n3 n4)
    (next n4 n5)
    
    ; Initial path length is zero
    (path-length n0)
    
    ; Total number of vertices
    (total-vertices n5)
  )
  
  (:goal
    (and
      ; We've returned to the start vertex
      (exists (?v - vertex) 
        (and (start ?v) (current ?v)))
      
      ; All vertices have been visited
      (visited v1)
      (visited v2)
      (visited v3)
      (visited v4)
      (visited v5)
      
      ; Path length equals total vertices
      (path-length n5)
    )
  )
)