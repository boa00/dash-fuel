# Dash Fueld home task

## Relationships diagram

<p align="center"><img src="https://i.ibb.co/KhJzPH3/Untitled-drawio.png" alt="Hello there!" width=400 height=420></p>


## API methods

1) Tanks
- GET /api/tanks?q={search_query_on_tank_name}
- POST /api/tanks
- GET, UPDATE, DELETE /api/tanks/id 
2) Tank Volumes
- GET /api/volumes?tank_id={tank_id}&order_by={order}&sort_by={column}
- POST /api/volumes
- GET, UPDATE, DELETE /api/tanks/id 
3) Tank Sales (table holds total sales for each day)
- GET /api/tank-sales?tank_id={tank_id}
- POST /api/tank-sales
- GET, UPDATE, DELETE /api/tank-sales/id 
4) Average Tank Sales (table holds the 5-week average for each day)
- GET /api/avg-tank-sales?tank_id={tank_id}
- POST /api/avg-tank-sales
- GET, UPDATE, DELETE /api/avg-tank-sales/id 
