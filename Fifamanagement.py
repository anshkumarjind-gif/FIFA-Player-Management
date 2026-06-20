import json
import os
from datetime import datetime

FILE_NAME = "FIFA.json"


def load_data():
    """Load player data from JSON file"""
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w") as file:
            json.dump([], file)
    
    try:
        with open(FILE_NAME, "r") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []


def save_data(players):
    """Save player data to JSON file"""
    try:
        with open(FILE_NAME, "w") as file:
            json.dump(players, file, indent=4)
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False


def generate_player_id(players):
    """Generate unique player ID"""
    if not players:
        return "FIFA001"
    
    max_num = 0
    for player in players:
        try:
            num = int(player["player_id"].replace("FIFA", ""))
            max_num = max(max_num, num)
        except (ValueError, KeyError):
            pass
    
    return f"FIFA{max_num + 1:03d}"


def register_player():
    """Register a new player"""
    players = load_data()
    
    print("\n" + "=" * 50)
    print("         PLAYER REGISTRATION")
    print("=" * 50)
    
    try:
        name = input("Enter Player Name: ").strip()
        if not name:
            print("❌ Player name cannot be empty!")
            return
        
        country = input("Enter Country: ").strip()
        if not country:
            print("❌ Country cannot be empty!")
            return
        
        score = int(input("Enter Score: "))
        world_cups = int(input("Enter World Cups Played: "))
        
        player = {
            "player_id": generate_player_id(players),
            "name": name,
            "country": country,
            "score": score,
            "total_world_cup_played": world_cups,
            "created_date": datetime.now().strftime("%Y-%m-%d")
        }
        
        players.append(player)
        
        if save_data(players):
            print("\n✅ Player Registered Successfully!")
            print(f"📋 Player ID: {player['player_id']}")
            print(f"👤 Name: {player['name']}")
            print(f"🌍 Country: {player['country']}")
        else:
            print("❌ Failed to save player data!")
    
    except ValueError:
        print("❌ Invalid input! Please enter numbers for Score and World Cups.")
    except Exception as e:
        print(f"❌ Error during registration: {e}")


def view_players():
    """Display all registered players"""
    players = load_data()
    
    print("\n" + "=" * 50)
    print("         ALL PLAYER SCORES")
    print("=" * 50)
    
    if not players:
        print("❌ No players found in the system.")
        return
    
    for index, player in enumerate(players, 1):
        print(f"\n{'─' * 50}")
        print(f"Player #{index}")
        print(f"📌 ID: {player['player_id']}")
        print(f"👤 Name: {player['name']}")
        print(f"🌍 Country: {player['country']}")
        print(f"⚽ Score: {player['score']}")
        print(f"🏆 World Cups: {player['total_world_cup_played']}")
        print(f"📅 Created: {player['created_date']}")
    
    print(f"\n{'─' * 50}")
    print(f"✅ Total Players: {len(players)}")


def search_player():
    """Search for a player by name or ID"""
    players = load_data()
    
    if not players:
        print("❌ No players found in the system.")
        return
    
    print("\n" + "=" * 50)
    print("         SEARCH PLAYER")
    print("=" * 50)
    
    keyword = input("Enter Player Name or ID: ").strip().lower()
    
    if not keyword:
        print("❌ Search keyword cannot be empty!")
        return
    
    found_players = []
    
    for player in players:
        if (player["player_id"].lower() == keyword or 
            player["name"].lower() == keyword or
            keyword in player["name"].lower()):
            found_players.append(player)
    
    if found_players:
        print(f"\n✅ Found {len(found_players)} player(s):\n")
        for player in found_players:
            print(f"{'─' * 50}")
            print(f"📌 ID: {player['player_id']}")
            print(f"👤 Name: {player['name']}")
            print(f"🌍 Country: {player['country']}")
            print(f"⚽ Score: {player['score']}")
            print(f"🏆 World Cups: {player['total_world_cup_played']}")
            print(f"📅 Created: {player['created_date']}")
    else:
        print(f"❌ No player found with name or ID: {keyword}")


def update_score():
    """Update a player's score"""
    players = load_data()
    
    if not players:
        print("❌ No players found in the system.")
        return
    
    print("\n" + "=" * 50)
    print("         UPDATE PLAYER SCORE")
    print("=" * 50)
    
    player_id = input("Enter Player ID: ").strip().upper()
    
    if not player_id:
        print("❌ Player ID cannot be empty!")
        return
    
    found = False
    
    for player in players:
        if player["player_id"] == player_id:
            found = True
            print(f"\n📌 Player Found: {player['name']}")
            print(f"📊 Current Score: {player['score']}")
            
            try:
                new_score = int(input("Enter New Score: "))
                old_score = player["score"]
                player["score"] = new_score
                
                if save_data(players):
                    difference = new_score - old_score
                    symbol = "📈" if difference >= 0 else "📉"
                    print(f"\n✅ Score Updated Successfully!")
                    print(f"📊 Previous Score: {old_score}")
                    print(f"📊 New Score: {new_score}")
                    print(f"{symbol} Change: {difference:+d}")
                else:
                    print("❌ Failed to save updated score!")
            except ValueError:
                print("❌ Invalid input! Please enter a valid number.")
            break
    
    if not found:
        print(f"❌ Player with ID '{player_id}' not found.")


def top_players():
    """Display top 2 players by score"""
    players = load_data()
    
    print("\n" + "=" * 50)
    print("         TOP 2 PLAYERS BY SCORE")
    print("=" * 50)
    
    if not players:
        print("❌ No players found in the system.")
        return
    
    if len(players) == 1:
        print("\n⚠️  Only 1 player in the system:\n")
        player = players[0]
        print(f"🥇 {player['name']} ({player['country']}) - Score: {player['score']}")
        return
    
    sorted_players = sorted(players, key=lambda x: x["score"], reverse=True)
    
    print("\n")
    medals = ["🥇", "🥈"]
    
    for index, player in enumerate(sorted_players[:2]):
        print(f"{medals[index]} Rank #{index + 1}")
        print(f"   👤 Name: {player['name']}")
        print(f"   🌍 Country: {player['country']}")
        print(f"   ⚽ Score: {player['score']}")
        print(f"   📌 ID: {player['player_id']}\n")


def main():
    """Main program loop"""
    while True:
        print("\n" + "=" * 50)
        print("   FIFA PLAYER MANAGEMENT SYSTEM")
        print("=" * 50)
        print("1. 👤 Player Registration")
        print("2. 📊 View All Player Scores")
        print("3. 🔍 Search Player")
        print("4. ✏️  Update Score")
        print("5. 🏆 Top 2 Players by Score")
        print("6. 🚪 Exit")
        print("=" * 50)
        
        choice = input("\nEnter Your Choice (1-6): ").strip()
        
        if choice == "1":
            register_player()
        
        elif choice == "2":
            view_players()
        
        elif choice == "3":
            search_player()
        
        elif choice == "4":
            update_score()
        
        elif choice == "5":
            top_players()
        
        elif choice == "6":
            print("\n" + "=" * 50)
            print("✅ Program Closed Successfully!")
            print("=" * 50 + "\n")
            break
        
        else:
            print("❌ Invalid Choice! Please enter a number between 1-6.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()