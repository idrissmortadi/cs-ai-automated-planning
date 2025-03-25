(define (problem hamiltonian-example)
  (:domain hamiltonian-cycle)
  
  (:objects
    {VERTEX_OBJECTS}
    {COUNT_OBJECTS}
  )
  
  (:init
    ; Define the graph structure (edges)
    {GRAPH_EDGES}
    
    ; Define the count sequence for tracking path length
    {COUNT_SEQUENCE}
    
    ; Initial path length is zero
    (path-length n0)
    
    ; No start vertex selected yet
    (not (start-selected))
    
    ; Total number of vertices
    (total-vertices {TOTAL_VERTICES})
  )
  
  (:goal
    (and
      ; We've returned to the start vertex
      (back-at-start)
      
      ; All vertices have been visited
      {VISITED_GOALS}
      
      ; Path length equals total vertices
      (path-length {TOTAL_VERTICES})
    )
  )
)