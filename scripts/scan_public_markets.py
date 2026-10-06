from bot.market_data import PolymarketPublicData

def main():
    rows = PolymarketPublicData().snapshots(limit=25)
    print("Markets with readable order books:", len(rows))
    for row in rows[:10]:
        print(row)

if __name__ == "__main__":
    main()
