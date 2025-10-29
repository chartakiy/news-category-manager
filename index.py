import psycopg2

class DataConnect:
  def __init__(self):
    self.connection = psycopg2.connect(
      dbname = 'n71__23_10',
      user = 'johnibek',
      password = '123john',
      host = 'localhost',
      port = 5433
    )
    self.cursor = self.connection.cursor()
    print('Connected to the database')
  
  def view_categories(self):
    query = "SELECT category_id, category_title FROM categories"
    self.cursor.execute(query)
    rows = self.cursor.fetchall()
    if not rows:
      print("no categories found")
    else:
      print("\n Categories list")
      for i, row in enumerate(rows, 1):
        category_id, category_title = row
        print(f"Category ID: {category_id}, Category Title: {category_title}")
  
  def add_category(self, category_id, category_title):
    query = "INSERT INTO categories VALUES (%s, %s, %s)"
    self.cursor.execute(query, (category_id, category_title))
    self.connection.commit()
    print(f"Category {category_title} added successfully")
  
  def edit_category(self, index):
    categories = self.view_categories()

    if not categories:
      return
    try:
      category = categories[index]
      category_id, category_title = category
      
      print(f"\nEditing category {category_title}")
      new_category_id = input("New Category ID (or leave it blank to keep current)") or category_id
      new_category_title = input("New Category Title (or leave it blank to keep current)") or category_title

      query = """
        UPDATE categories
        SET category_id=%s, category_title=%s
        WHERE category_id=%s, category_title=%s
      """
      self.cursor.execute(query, (new_category_id, new_category_title, category_id, category_title))
      self.connection.commit()
      print("Category updated successfully")
    except IndexError:
      print("Invalid Index")
  
  def delete_category(self, index):
    categories = self.view_categories()

    if not categories:
      return
    try:
      category = categories[index]
      category_id, category_title = category

      query = """
        DELETE FROM categories
        WHERE category_id=%s, category_title=%s
      """
      self.cursor.execute(query, (category_id, category_title))
      self.connection.commit()
      print("Category deleted successfully")
    except IndexError:
      print('Invalid Index')
  
  # def view_news(self):
  #   query = "SELECT news_id, news_title, news_content, date_created, date_updated FROM news"
  #   self.cursor.execute(query)
  #   rows = self.cursor.fetchall()
  #   if not rows:
  #     print("no news found")
  #   else:
  #     print("\n News list")
  #     for i, row in enumerate(rows, 1):
  #       news_id, news_title, news_content, date_created, date_updated = row
  #       print(f"News ID: {news_id}, \nNews Content: {news_content}, \nDate Created: {date_created}, Date Updated: {date_updated}")



def main():
  db = DataConnect()

  while True:
    print("\n ======================= Main Menu ======================= ")
    print("1. Categories\n2. News\n3. Exit")

    choice = input("choose an option: ")

    if choice == "1":
      print("welcome to categories")
    elif choice == "2":
      print("welcome to News")
    elif choice == "3":
      print("exiting the program")
    else:
      print("invalid choice, try again")

if __name__ == "__main__":
  main()