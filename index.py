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
  
  # def view_categories(self):
  #   query = "SELECT category_id, category_title FROM categories"
  #   self.cursor.execute(query)
  #   rows = self.cursor.fetchall()
  #   if not rows:
  #     print("no categories found")
  #   else:
  #     print("\n Categories list")
  #     for i, row in enumerate(rows, 1):
  #       category_id, category_title = row
  #       print(f"Category ID: {category_id}, Category Title: {category_title}")
    
  #   return rows

  def view_categories(self):
    query = "SELECT category_id, category_title FROM categories"
    self.cursor.execute(query)
    rows = self.cursor.fetchall()

    if not rows:
        print("No categories found.")
    else:
        print("\n========== Categories List ==========")
        for i, row in enumerate(rows, 1):
            category_id, category_title = row
            print(f"{i}. {category_title} (ID: {category_id})")
        print("=====================================")
    
    return rows 
  
  def add_category(self, category_id, category_title):
    query = "INSERT INTO categories VALUES (%s, %s)"
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
      new_category_id = input("New Category ID (or leave it blank to keep current): ") or category_id
      new_category_title = input("New Category Title (or leave it blank to keep current): ") or category_title

      query = """
        UPDATE categories
        SET category_title=%s, category_id=%s
        WHERE category_id=%s AND category_title=%s
      """
      self.cursor.execute(query, (new_category_title, new_category_id, category_id, category_title))
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
        WHERE category_id=%s AND category_title=%s
      """
      self.cursor.execute(query, (category_id, category_title))
      self.connection.commit()
      print("Category deleted successfully")
    except IndexError:
      print('Invalid Index')
  
  def view_news(self):
    query = "SELECT news_id, news_title, news_content, date_created, date_updated FROM news"
    self.cursor.execute(query)
    rows = self.cursor.fetchall()
    if not rows:
      print("no news found")
    else:
      print("\nAll News Headlines")
      for i, row in enumerate(rows, 1):
        news_id, news_title, news_content, date_created, date_updated = row
        print(f"{i}. {news_title} ({date_updated if date_updated else date_created})")

      while True:
        choice = input("\nEnter the index of news you would like to read (or type 'b' to to go back): ")

        if choice.lower() == 'b':
          break
        
        if not choice.isdigit():
          print("Pls, enter a valid number")
          continue

        index = int(choice)
        if 1 <= index <= len(rows):
          news_id, news_title, news_content, date_created, date_updated = row[index - 1]
          print(f"\nHeadline: {news_title}\n{news_content}")
          print(f"\n Date Created: {date_created}, Date Updated: {date_updated}")
        else:
          print("Invalid number, pls input a valid one from the list above")
  
  def add_news(self, news_id, category_id, news_title, news_content, date_created, date_updated):
    query = "INSERT INTO news VALUES (%s, %s, %s, %s, %s, %s)"
    self.cursor.execute(query, (news_id, category_id, news_title, news_content, date_created, date_updated))
    self.connection.commit()
    print(f"News {news_title} added successfully")
  
  def edit_news(self, index):
    news = self.view_news()

    if not news:
      return
    
    try:
      a_news = news[index]
      news_id, news_title, news_content = a_news
      print("\nEditing news")
      new_title = input("New title (leave blank to keep current): ") or news_title
      new_content = input("New content (leave blank to keep current): ") or news_content
      query = """
        UPDATE news
        SET news_title=%s, news_content=%s
        WHERE news_id=%s
      """
      self.cursor.execute(query, (news_title, news_content, news_id))
      self.connection.commit()
      print("News updated successfully")
    
    except IndexError:
      print("pls, enter a valid index")

  def delete_news(self, index):
    news = self.view_news()

    if not news:
      return
    
    try:
      a_news = news[index]
      news_id, news_title, news_content = a_news
      query = "DELETE FROM news WHERE news_id=%s"
      self.cursor.execute(query, (news_id))
      self.connection.commit()
      print("News deleted successfully")


    except IndexError:
      print("pls, enter a valid index")


def category_manager(db):
  while True:
    print("\n ======================= Category Manager ======================= ")
    print("1. View Categories\n2. Add a category\n3. Edit a category\n4. Delete a category\n5. Go Back")
    choice = input("your choice: ")

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
          index = int(input("Enter news number to update: ")) - 1
          db.edit_category(index)
        except ValueError:
          print("Please enter a valid number.")
    elif choice == '4':
      categories = db.view_categories()
      if categories:
        try:
          index = int(input("Enter news number to delete: ")) - 1
          db.delete_category(index)
        except ValueError:
          print("Please enter a valid number.")


def main():
  db = DataConnect()

  while True:
    print("\n ======================= Main Menu ======================= ")
    print("1. Categories\n2. News\n3. Exit")

    choice = input("choose an option: ")

    if choice == "1":
      category_manager(db)
    elif choice == "2":
      print("welcome to News")
    elif choice == "3":
      print("exiting the program")
    else:
      print("invalid choice, try again")

if __name__ == "__main__":
  main()