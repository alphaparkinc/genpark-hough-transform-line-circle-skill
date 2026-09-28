import sys
import json
from client import HoughTransformEngine

def handle_rpc(line):
    try:
        req = json.loads(line)
    except Exception:
        return
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        res = {
            "protocolVersion": "2024-11-05",
            "serverInfo": {"name": "genpark-hough-transform-line-circle-skill", "version": "1.0.0"},
            "capabilities": {"tools": {}}
        }
    elif method == "tools/list":
        res = {
            "tools": [
                {
                    "name": "detect_lines",
                    "description": "Extract straight line parameters (rho, theta) from binary edge map using Hough transform",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "edge_image": {"type": "array", "items": {"type": "array", "items": {"type": "integer"}}},
                            "threshold": {"type": "integer", "default": 10}
                        },
                        "required": ["edge_image"]
                    }
                }
            ]
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "detect_lines":
            engine = HoughTransformEngine()
            data = engine.detect_lines(args.get("edge_image", []), threshold=args.get("threshold", 10))
            res = {"content": [{"type": "text", "text": json.dumps(data)}]}
        else:
            res = {"isError": True, "content": [{"type": "text", "text": f"Unknown tool {tool_name}"}]}
    else:
        res = {"error": {"code": -32601, "message": "Method not found"}}

    resp = {"jsonrpc": "2.0", "id": req_id, "result": res.get("result", res)}
    sys.stdout.write(json.dumps(resp) + "\n")
    sys.stdout.flush()

def main():
    for line in sys.stdin:
        if line.strip():
            handle_rpc(line.strip())

if __name__ == "__main__":
    main()
