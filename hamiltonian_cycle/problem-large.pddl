(define (problem hamiltonian-example)
  (:domain hamiltonian-cycle)
  
  (:objects
    v1 v2 v3 v4 v5 v6 v7 v8 v9 v10 v11 v12 v13 v14 v15 v16 v17 v18 v19 v20 v21 v22 v23 v24 v25 v26 v27 v28 v29 v30 - vertex
    n0 n1 n2 n3 n4 n5 n6 n7 n8 n9 n10 n11 n12 n13 n14 n15 n16 n17 n18 n19 n20 n21 n22 n23 n24 n25 n26 n27 n28 n29 n30 - count
  )
  
  (:init
    ; Define the graph structure (edges)
        (connected v1 v10)
    (connected v10 v1)
    (connected v1 v14)
    (connected v14 v1)
    (connected v1 v18)
    (connected v18 v1)
    (connected v1 v19)
    (connected v19 v1)
    (connected v1 v23)
    (connected v23 v1)
    (connected v1 v30)
    (connected v30 v1)
    (connected v2 v3)
    (connected v3 v2)
    (connected v2 v4)
    (connected v4 v2)
    (connected v2 v5)
    (connected v5 v2)
    (connected v2 v8)
    (connected v8 v2)
    (connected v2 v12)
    (connected v12 v2)
    (connected v2 v16)
    (connected v16 v2)
    (connected v2 v18)
    (connected v18 v2)
    (connected v2 v19)
    (connected v19 v2)
    (connected v2 v21)
    (connected v21 v2)
    (connected v2 v22)
    (connected v22 v2)
    (connected v2 v28)
    (connected v28 v2)
    (connected v2 v30)
    (connected v30 v2)
    (connected v3 v6)
    (connected v6 v3)
    (connected v3 v8)
    (connected v8 v3)
    (connected v3 v12)
    (connected v12 v3)
    (connected v3 v13)
    (connected v13 v3)
    (connected v3 v14)
    (connected v14 v3)
    (connected v3 v16)
    (connected v16 v3)
    (connected v3 v18)
    (connected v18 v3)
    (connected v3 v19)
    (connected v19 v3)
    (connected v3 v23)
    (connected v23 v3)
    (connected v3 v28)
    (connected v28 v3)
    (connected v4 v5)
    (connected v5 v4)
    (connected v4 v6)
    (connected v6 v4)
    (connected v4 v8)
    (connected v8 v4)
    (connected v4 v14)
    (connected v14 v4)
    (connected v4 v16)
    (connected v16 v4)
    (connected v4 v20)
    (connected v20 v4)
    (connected v4 v23)
    (connected v23 v4)
    (connected v4 v24)
    (connected v24 v4)
    (connected v4 v26)
    (connected v26 v4)
    (connected v4 v28)
    (connected v28 v4)
    (connected v5 v7)
    (connected v7 v5)
    (connected v5 v12)
    (connected v12 v5)
    (connected v5 v14)
    (connected v14 v5)
    (connected v5 v17)
    (connected v17 v5)
    (connected v5 v20)
    (connected v20 v5)
    (connected v5 v21)
    (connected v21 v5)
    (connected v5 v22)
    (connected v22 v5)
    (connected v5 v23)
    (connected v23 v5)
    (connected v5 v24)
    (connected v24 v5)
    (connected v5 v29)
    (connected v29 v5)
    (connected v6 v7)
    (connected v7 v6)
    (connected v6 v10)
    (connected v10 v6)
    (connected v6 v13)
    (connected v13 v6)
    (connected v6 v14)
    (connected v14 v6)
    (connected v6 v18)
    (connected v18 v6)
    (connected v6 v21)
    (connected v21 v6)
    (connected v6 v26)
    (connected v26 v6)
    (connected v6 v27)
    (connected v27 v6)
    (connected v6 v30)
    (connected v30 v6)
    (connected v7 v8)
    (connected v8 v7)
    (connected v7 v11)
    (connected v11 v7)
    (connected v7 v14)
    (connected v14 v7)
    (connected v7 v16)
    (connected v16 v7)
    (connected v7 v17)
    (connected v17 v7)
    (connected v7 v19)
    (connected v19 v7)
    (connected v7 v20)
    (connected v20 v7)
    (connected v7 v22)
    (connected v22 v7)
    (connected v7 v24)
    (connected v24 v7)
    (connected v7 v26)
    (connected v26 v7)
    (connected v7 v30)
    (connected v30 v7)
    (connected v8 v12)
    (connected v12 v8)
    (connected v8 v13)
    (connected v13 v8)
    (connected v8 v14)
    (connected v14 v8)
    (connected v8 v15)
    (connected v15 v8)
    (connected v8 v18)
    (connected v18 v8)
    (connected v8 v21)
    (connected v21 v8)
    (connected v8 v22)
    (connected v22 v8)
    (connected v8 v23)
    (connected v23 v8)
    (connected v8 v24)
    (connected v24 v8)
    (connected v9 v10)
    (connected v10 v9)
    (connected v9 v18)
    (connected v18 v9)
    (connected v9 v19)
    (connected v19 v9)
    (connected v9 v20)
    (connected v20 v9)
    (connected v9 v22)
    (connected v22 v9)
    (connected v9 v27)
    (connected v27 v9)
    (connected v9 v29)
    (connected v29 v9)
    (connected v10 v11)
    (connected v11 v10)
    (connected v10 v12)
    (connected v12 v10)
    (connected v10 v13)
    (connected v13 v10)
    (connected v10 v16)
    (connected v16 v10)
    (connected v10 v17)
    (connected v17 v10)
    (connected v10 v21)
    (connected v21 v10)
    (connected v10 v25)
    (connected v25 v10)
    (connected v10 v29)
    (connected v29 v10)
    (connected v10 v30)
    (connected v30 v10)
    (connected v11 v12)
    (connected v12 v11)
    (connected v11 v14)
    (connected v14 v11)
    (connected v11 v17)
    (connected v17 v11)
    (connected v11 v20)
    (connected v20 v11)
    (connected v11 v22)
    (connected v22 v11)
    (connected v11 v23)
    (connected v23 v11)
    (connected v11 v24)
    (connected v24 v11)
    (connected v11 v25)
    (connected v25 v11)
    (connected v11 v26)
    (connected v26 v11)
    (connected v11 v27)
    (connected v27 v11)
    (connected v12 v13)
    (connected v13 v12)
    (connected v12 v15)
    (connected v15 v12)
    (connected v12 v19)
    (connected v19 v12)
    (connected v12 v21)
    (connected v21 v12)
    (connected v12 v22)
    (connected v22 v12)
    (connected v13 v16)
    (connected v16 v13)
    (connected v13 v19)
    (connected v19 v13)
    (connected v13 v26)
    (connected v26 v13)
    (connected v13 v30)
    (connected v30 v13)
    (connected v14 v15)
    (connected v15 v14)
    (connected v14 v16)
    (connected v16 v14)
    (connected v14 v17)
    (connected v17 v14)
    (connected v14 v18)
    (connected v18 v14)
    (connected v14 v19)
    (connected v19 v14)
    (connected v14 v20)
    (connected v20 v14)
    (connected v14 v21)
    (connected v21 v14)
    (connected v14 v22)
    (connected v22 v14)
    (connected v14 v23)
    (connected v23 v14)
    (connected v14 v25)
    (connected v25 v14)
    (connected v14 v29)
    (connected v29 v14)
    (connected v15 v16)
    (connected v16 v15)
    (connected v15 v18)
    (connected v18 v15)
    (connected v15 v19)
    (connected v19 v15)
    (connected v15 v22)
    (connected v22 v15)
    (connected v15 v23)
    (connected v23 v15)
    (connected v15 v25)
    (connected v25 v15)
    (connected v15 v26)
    (connected v26 v15)
    (connected v15 v27)
    (connected v27 v15)
    (connected v15 v28)
    (connected v28 v15)
    (connected v15 v29)
    (connected v29 v15)
    (connected v15 v30)
    (connected v30 v15)
    (connected v16 v18)
    (connected v18 v16)
    (connected v16 v20)
    (connected v20 v16)
    (connected v16 v22)
    (connected v22 v16)
    (connected v16 v29)
    (connected v29 v16)
    (connected v16 v30)
    (connected v30 v16)
    (connected v17 v30)
    (connected v30 v17)
    (connected v18 v22)
    (connected v22 v18)
    (connected v18 v23)
    (connected v23 v18)
    (connected v18 v26)
    (connected v26 v18)
    (connected v18 v28)
    (connected v28 v18)
    (connected v18 v30)
    (connected v30 v18)
    (connected v19 v20)
    (connected v20 v19)
    (connected v19 v21)
    (connected v21 v19)
    (connected v19 v24)
    (connected v24 v19)
    (connected v19 v25)
    (connected v25 v19)
    (connected v19 v28)
    (connected v28 v19)
    (connected v19 v30)
    (connected v30 v19)
    (connected v20 v21)
    (connected v21 v20)
    (connected v20 v23)
    (connected v23 v20)
    (connected v20 v24)
    (connected v24 v20)
    (connected v20 v25)
    (connected v25 v20)
    (connected v21 v25)
    (connected v25 v21)
    (connected v21 v29)
    (connected v29 v21)
    (connected v21 v30)
    (connected v30 v21)
    (connected v22 v26)
    (connected v26 v22)
    (connected v22 v27)
    (connected v27 v22)
    (connected v22 v28)
    (connected v28 v22)
    (connected v22 v29)
    (connected v29 v22)
    (connected v23 v26)
    (connected v26 v23)
    (connected v24 v25)
    (connected v25 v24)
    (connected v24 v27)
    (connected v27 v24)
    (connected v24 v28)
    (connected v28 v24)
    (connected v25 v27)
    (connected v27 v25)
    (connected v25 v29)
    (connected v29 v25)
    (connected v25 v30)
    (connected v30 v25)
    (connected v26 v29)
    (connected v29 v26)
    
    ; Define the count sequence for tracking path length
        (next n0 n1)
    (next n1 n2)
    (next n2 n3)
    (next n3 n4)
    (next n4 n5)
    (next n5 n6)
    (next n6 n7)
    (next n7 n8)
    (next n8 n9)
    (next n9 n10)
    (next n10 n11)
    (next n11 n12)
    (next n12 n13)
    (next n13 n14)
    (next n14 n15)
    (next n15 n16)
    (next n16 n17)
    (next n17 n18)
    (next n18 n19)
    (next n19 n20)
    (next n20 n21)
    (next n21 n22)
    (next n22 n23)
    (next n23 n24)
    (next n24 n25)
    (next n25 n26)
    (next n26 n27)
    (next n27 n28)
    (next n28 n29)
    (next n29 n30)
    
    ; Initial path length is zero
    (path-length n0)
    
    ; Total number of vertices
    (total-vertices n30)
  )
  
  (:goal
    (and
      ; We've returned to the start vertex
      (back-at-start) 

      ; All vertices have been visited
      (visited v1)
      (visited v2)
      (visited v3)
      (visited v4)
      (visited v5)
      (visited v6)
      (visited v7)
      (visited v8)
      (visited v9)
      (visited v10)
      (visited v11)
      (visited v12)
      (visited v13)
      (visited v14)
      (visited v15)
      (visited v16)
      (visited v17)
      (visited v18)
      (visited v19)
      (visited v20)
      (visited v21)
      (visited v22)
      (visited v23)
      (visited v24)
      (visited v25)
      (visited v26)
      (visited v27)
      (visited v28)
      (visited v29)
      (visited v30)
      
      ; Path length equals total vertices
      (path-length n30)
    )
  )
)