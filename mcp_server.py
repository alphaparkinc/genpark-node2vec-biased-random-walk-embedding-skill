import sys
import json
from client import Node2VecWalkGenerator

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-node2vec-biased-random-walk-embedding-skill", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "generate_node2vec_walks",
                        "description": "Generate 2nd-order biased random walk sequences for graph embedding",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "adjacency": {"type": "object"},
                                "start_node": {"type": "string"},
                                "num_walks": {"type": "integer", "default": 3},
                                "walk_length": {"type": "integer", "default": 6},
                                "p": {"type": "number", "default": 1.0},
                                "q": {"type": "number", "default": 1.0}
                            },
                            "required": ["adjacency", "start_node"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        
        if tool_name == "generate_node2vec_walks":
            adj = args.get("adjacency", {})
            start = args.get("start_node")
            p = args.get("p", 1.0)
            q = args.get("q", 1.0)
            wl = args.get("walk_length", 6)
            nw = args.get("num_walks", 3)
            gen = Node2VecWalkGenerator(adj, p=p, q=q)
            walks = [gen.generate_walk(start, walk_length=wl) for _ in range(nw)]
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps({"walks": walks})}]
                }
            }
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
