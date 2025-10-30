import psycopg2
from datetime import datetime
import random

class DataConnect:
  def __init__(self):
    self.connection = psycopg2.connect(
      dbname='n71__23_10',
      user='johnibek',
      password='123john',
      host='localhost',
      port=5433
    )
    self.cursor = self.connection.cursor()
    print('Connected to the database')

  def view_categories(self):
    query = "SELECT category_id, category_title FROM categories"
    self.cursor.execute(query)
    rows = self.cursor.fetchall()
    if not rows:
      print("No categories found.")
    else:
      print("\nCategories List:")
      for i, row in enumerate(rows, 1):
        category_id, category_title = row
        print(f"{i}. Category ID: {category_id}, Category Title: {category_title}")
    return rows

  def add_category(self, category_id, category_title):
    query = "INSERT INTO categories (category_id, category_title) VALUES (%s, %s)"
    self.cursor.execute(query, (category_id, category_title))
    self.connection.commit()
    print(f"Category '{category_title}' added successfully.")

  def edit_category(self, index):
    categories = self.view_categories()
    if not categories:
      return
    try:
      category = categories[index]
      category_id, category_title = category
      print(f"\nEditing category '{category_title}'")
      new_category_id = input("New Category ID (leave blank to keep current): ").strip() or category_id
      new_category_title = input("New Category Title (leave blank to keep current): ").strip() or category_title
      query = """
        UPDATE categories
        SET category_id=%s, category_title=%s
        WHERE category_id=%s AND category_title=%s
      """
      self.cursor.execute(query, (new_category_id, new_category_title, category_id, category_title))
      self.connection.commit()
      print("Category updated successfully.")
    except IndexError:
      print("Invalid index.")

  def delete_category(self, index):
    categories = self.view_categories()
    if not categories:
      return
    try:
      category = categories[index]
      category_id, category_title = category
      confirm = input(f"Are you sure you want to delete category '{category_title}' and all its news? (y/N): ").strip().lower()
      if confirm != 'y':
        print("Delete cancelled.")
        return
      self.cursor.execute("DELETE FROM categories WHERE category_id = %s;", (category_id,))
      self.connection.commit()
      print(f"Category '{category_title}' and all related news deleted successfully.")
    except IndexError:
      print("Invalid Index")

  def view_news(self, interactive=True):
    query = """
      SELECT n.news_id, n.category_id, c.category_title, n.news_title, n.news_content, n.date_created, n.date_updated
      FROM news n
      JOIN categories c ON n.category_id = c.category_id
    """
    self.cursor.execute(query)
    rows = self.cursor.fetchall()
    if not rows:
      print("No news found.")
      return rows
    print("\nAll News Headlines")
    for i, row in enumerate(rows, 1):
      _, _, category_title, news_title, _, date_created, date_updated = row
      print(f"{i}. [{category_title}] {news_title} ({date_updated if date_updated else date_created})")
    if not interactive:
      return rows
    while True:
      choice = input("\nEnter the number of the news you would like to read (or 'b' to go back): ").strip()
      if choice.lower() == 'b':
        break
      if not choice.isdigit():
        print("Please enter a valid number.")
        continue
      index = int(choice)
      if 1 <= index <= len(rows):
        news_id, category_id, category_title, news_title, news_content, date_created, date_updated = rows[index - 1]
        print("\n===============================")
        print(f"[{category_title}] {news_title}\n")
        print(news_content)
        print(f"\nDate Created: {date_created}")
        if date_updated:
          print(f"Date Updated: {date_updated}")
        print("===============================\n")
      else:
        print("Invalid number; enter one from the list above.")
    return rows

  def add_news(self, category_id, news_title, news_content):
    news_id = str(random.randint(10000000, 99999999))
    date_created = datetime.now()
    date_updated = None
    query = """
      INSERT INTO news (news_id, category_id, news_title, news_content, date_created, date_updated)
      VALUES (%s, %s, %s, %s, %s, %s)
    """
    self.cursor.execute(query, (news_id, category_id, news_title, news_content, date_created, date_updated))
    self.connection.commit()
    print(f"News '{news_title}' added successfully.")

  def edit_news(self, index):
    rows = self.view_news(interactive=False)
    if not rows:
      return
    try:
      row = rows[index]
      news_id, category_id, category_title, news_title, news_content, date_created, date_updated = row
      print("\nEditing news:")
      print(f"Current title: {news_title}")
      print(f"Current content: {news_content[:80]}{'...' if len(news_content) > 80 else ''}")
      new_title = input("New title (leave blank to keep current): ").strip() or news_title
      new_content = input("New content (leave blank to keep current): ").strip() or news_content
      new_updated = datetime.now()
      query = """
        UPDATE news
        SET news_title = %s, news_content = %s, date_updated = %s
        WHERE news_id = %s
      """
      self.cursor.execute(query, (new_title, new_content, new_updated, news_id))
      self.connection.commit()
      print("News updated successfully.")
    except IndexError:
      print("Please enter a valid index.")

  def delete_news(self, index):
    rows = self.view_news(interactive=False)
    if not rows:
      return
    try:
      row = rows[index]
      news_id, category_id, category_title, news_title, news_content, date_created, date_updated = row
      confirm = input(f"Are you sure you want to delete '{news_title}'? (y/N): ").strip().lower()
      if confirm != 'y':
        print("Delete cancelled.")
        return
      query = "DELETE FROM news WHERE news_id = %s"
      self.cursor.execute(query, (news_id,))
      self.connection.commit()
      print("News deleted successfully.")
    except IndexError:
      print("Please enter a valid index.")

def category_manager(db):
  while True:
    print("\n ======================= Category Manager ======================= ")
    print("1. View Categories\n2. Add a category\n3. Edit a category\n4. Delete a category\n5. Go Back")
    choice = input("Your choice: ")
    if choice == '1':
      db.view_categories()
    elif choice == '2':
      category_id = input("Category ID: ")
      category_title = input("Category Title: ")
      db.add_category(category_id, category_title)
    elif choice == '3':
      categories = db.view_categories()
      if categories:
        try:
          index = int(input("Enter category number to update: ")) - 1
          db.edit_category(index)
        except ValueError:
          print("Please enter a valid number.")
    elif choice == '4':
      categories = db.view_categories()
      if categories:
        try:
          index = int(input("Enter category number to delete: ")) - 1
          db.delete_category(index)
        except ValueError:
          print("Please enter a valid number.")
    elif choice == "5":
      break
    else:
      print("Invalid choice. Try again.")

def news_manager(db):
  while True:
    print("\n ======================= News Manager ======================= ")
    print("1. View All News\n2. Add News\n3. Edit News\n4. Delete News\n5. Go Back")
    choice = input("Your choice: ")
    if choice == '1':
      db.view_news()
    elif choice == '2':
      category_id = input("Category ID: ").strip()
      news_title = input("News Title: ").strip()
      news_content = input("News Content: ").strip()
      if not category_id or not news_title or not news_content:
        print("Please fill in all required fields.")
        continue
      db.add_news(category_id, news_title, news_content)
    elif choice == '3':
      news = db.view_news(interactive=False)
      if news:
        try:
          index = int(input("Enter news number to update: ")) - 1
          db.edit_news(index)
        except ValueError:
          print("Please enter a valid number.")
    elif choice == '4':
      news = db.view_news(interactive=False)
      if news:
        try:
          index = int(input("Enter news number to delete: ")) - 1
          db.delete_news(index)
        except ValueError:
          print("Please enter a valid number.")
    elif choice == "5":
      break
    else:
      print("Invalid choice. Try again.")

def main():
  db = DataConnect()
  while True:
    print("\n ======================= Main Menu ======================= ")
    print("1. Categories\n2. News\n3. Exit")
    choice = input("Choose an option: ")
    if choice == "1":
      category_manager(db)
    elif choice == "2":
      news_manager(db)
    elif choice == "3":
      print("Exiting the program.")
      break
    else:
      print("Invalid choice, try again.")

if __name__ == "__main__":
  main()