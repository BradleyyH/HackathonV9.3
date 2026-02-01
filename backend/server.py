import asyncio
import websockets
import json
import uuid
from game_logic import MultiplayerSnakeGame

class GameServer:
    def __init__(self, grid_width=20, grid_height=20):
        self.game = MultiplayerSnakeGame(grid_width, grid_height)
        self.host_connection = None
        self.fruit_connections = {}  # player_id -> websocket
        self.game_loop_task = None
        self.game_speed = 0.15  # seconds between updates (about 6-7 FPS)
    
    async def register_host(self, websocket):
        """Register the host (snake player)."""
        if self.host_connection is None:
            self.host_connection = websocket
            await self.send_to_host({'type': 'host_registered', 'status': 'success'})
            print("Host registered")
        else:
            await websocket.send(json.dumps({'type': 'error', 'message': 'Host already registered'}))
            await websocket.close()
    
    async def register_fruit_player(self, websocket):
        """Register a new fruit player."""
        player_id = str(uuid.uuid4())
        self.fruit_connections[player_id] = websocket
        self.game.add_fruit_player(player_id)
        
        await websocket.send(json.dumps({
            'type': 'player_registered',
            'player_id': player_id,
            'grid_width': self.game.grid_width,
            'grid_height': self.game.grid_height
        }))
        
        print(f"Fruit player registered: {player_id}")
        return player_id
    
    async def handle_host_message(self, message):
        """Handle message from host (snake player)."""
        try:
            data = json.loads(message)
            msg_type = data.get('type')
            
            if msg_type == 'direction':
                direction = data.get('direction')
                self.game.set_direction(direction)
            elif msg_type == 'reset':
                self.game.reset()
                await self.broadcast_game_state()
        except json.JSONDecodeError:
            print("Invalid JSON from host")
    
    async def handle_fruit_message(self, player_id, message):
        """Handle message from fruit player."""
        try:
            data = json.loads(message)
            msg_type = data.get('type')
            
            if msg_type == 'move':
                x = data.get('x')
                y = data.get('y')
                self.game.update_fruit_position(player_id, x, y)
                # Broadcast updated state immediately when fruit moves
                await self.broadcast_game_state()
        except json.JSONDecodeError:
            print(f"Invalid JSON from fruit player {player_id}")
    
    async def send_to_host(self, message):
        """Send message to host."""
        if self.host_connection:
            try:
                await self.host_connection.send(json.dumps(message))
            except websockets.exceptions.ConnectionClosed:
                self.host_connection = None
    
    async def send_to_fruit_player(self, player_id, message):
        """Send message to a specific fruit player."""
        if player_id in self.fruit_connections:
            try:
                await self.fruit_connections[player_id].send(json.dumps(message))
            except websockets.exceptions.ConnectionClosed:
                # Remove disconnected player
                del self.fruit_connections[player_id]
                self.game.remove_fruit_player(player_id)
    
    async def broadcast_game_state(self):
        """Broadcast current game state to all connected clients."""
        game_state = self.game.get_game_state()
        
        # Send to host
        await self.send_to_host({
            'type': 'game_state',
            **game_state
        })
        
        # Send to all fruit players
        for player_id in list(self.fruit_connections.keys()):
            # Send state with their specific fruit position highlighted
            await self.send_to_fruit_player(player_id, {
                'type': 'game_state',
                **game_state,
                'your_player_id': player_id
            })
    
    async def game_loop(self):
        """Main game loop that updates the game state."""
        while True:
            await asyncio.sleep(self.game_speed)
            
            if self.host_connection:  # Only update if host is connected
                self.game.update()
                await self.broadcast_game_state()
                
                # If game over, notify all clients
                if self.game.game_over:
                    await self.send_to_host({
                        'type': 'game_over',
                        'score': self.game.score
                    })
                    for player_id in list(self.fruit_connections.keys()):
                        await self.send_to_fruit_player(player_id, {
                            'type': 'game_over',
                            'score': self.game.score
                        })
    
    async def handle_client(self, websocket, path=None):
        """Handle a new client connection."""
        client_type = None
        player_id = None
        
        try:
            # Wait for initial message to determine client type
            initial_message = await websocket.recv()
            data = json.loads(initial_message)
            client_type = data.get('type')
            
            if client_type == 'host':
                await self.register_host(websocket)
                # Start game loop if not already running
                if self.game_loop_task is None or self.game_loop_task.done():
                    self.game_loop_task = asyncio.create_task(self.game_loop())
                
                # Send initial game state
                await self.broadcast_game_state()
                
                # Handle host messages
                async for message in websocket:
                    await self.handle_host_message(message)
            
            elif client_type == 'fruit_player':
                player_id = await self.register_fruit_player(websocket)
                # Send initial game state
                await self.broadcast_game_state()
                
                # Handle fruit player messages
                async for message in websocket:
                    await self.handle_fruit_message(player_id, message)
            
            else:
                await websocket.send(json.dumps({
                    'type': 'error',
                    'message': 'Invalid client type. Use "host" or "fruit_player"'
                }))
                await websocket.close()
        
        except websockets.exceptions.ConnectionClosed:
            print(f"Client disconnected: {client_type}, player_id: {player_id}")
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            # Cleanup
            if client_type == 'host':
                self.host_connection = None
            elif client_type == 'fruit_player' and player_id:
                if player_id in self.fruit_connections:
                    del self.fruit_connections[player_id]
                self.game.remove_fruit_player(player_id)

async def main():
    server = GameServer(grid_width=20, grid_height=20)
    
    print("Starting WebSocket server on ws://localhost:8765")
    print("Host should connect first, then fruit players can join")
    
    # Create a wrapper function to handle the websocket connection
    async def handler(websocket, path=None):
        await server.handle_client(websocket, path)
    
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
