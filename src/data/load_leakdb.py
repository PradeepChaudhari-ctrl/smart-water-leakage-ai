from water_benchmark_hub import load


def main():
    print("Loading LeakDB...")

    leakdb = load("KIOS-LeakDB")

    X, y_leak = leakdb.load_data(
        scenarios_id=list(range(10)),
        use_net1=True,
        return_X_y=True
    )

    print("\nDataset loaded successfully!")
    print("X type:", type(X))
    print("y type:", type(y_leak))

    if hasattr(X, "shape"):
        print("X shape:", X.shape)

    if hasattr(y_leak, "shape"):
        print("y shape:", y_leak.shape)

    if hasattr(X, "dtype"):
        print("X dtype:", X.dtype)

    if hasattr(y_leak, "dtype"):
        print("y dtype:", y_leak.dtype)

    print("Unique labels:", set(y_leak.flatten().tolist()))


if __name__ == "__main__":
    main()
