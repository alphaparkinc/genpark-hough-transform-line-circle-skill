from client import HoughTransformEngine

def main():
    engine = HoughTransformEngine()
    edge_map = [[0]*20 for _ in range(20)]
    for i in range(5, 18):
        edge_map[7][i] = 255
    res = engine.detect_lines(edge_map, threshold=10)
    print("Hough Transform Line Detection Verification:")
    print(f"Detected Lines: {res['lines_count']}")
    for l in res['top_lines']:
        print(f"  Rho: {l['rho']}, Theta: {l['theta_rad']} rad, Votes: {l['votes']}")

if __name__ == "__main__":
    main()
