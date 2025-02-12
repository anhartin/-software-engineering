import tkinter as tk
import random

# Настройки игры
WIDTH, HEIGHT = 400, 400  # Размер окна
CELL_SIZE = 20  # Размер клетки
SPEED = 100  # Скорость змейки (меньше — быстрее)

# Направления
DIRECTIONS = {
    "Up": (0, -1),
    "Down": (0, 1),
    "Left": (-1, 0),
    "Right": (1, 0),
}

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Змейка")
        
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()

        self.label = tk.Label(root, text="Счет: 0", font=("Arial", 14))
        self.label.pack()

        self.start_button = tk.Button(root, text="Начать игру", font=("Arial", 14), command=self.start_game)
        self.start_button.pack()

        self.running = False
        self.root.bind("<KeyPress>", self.change_direction)

    def start_game(self):
        """Запускает новую игру"""
        self.start_button.pack_forget()  # Скрываем кнопку
        self.running = True
        self.snake = [(WIDTH // 2, HEIGHT // 2)]  # Начальная змейка
        self.direction = "Right"
        self.food = self.spawn_food()
        self.score = 0
        self.label.config(text=f"Счет: {self.score}")
        self.update()

    def spawn_food(self):
        """Создает еду в случайном месте, избегая змейки"""
        while True:
            x = random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE
            y = random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
            if (x, y) not in self.snake:
                return (x, y)

    def change_direction(self, event):
        """Меняет направление движения змейки"""
        if event.keysym in DIRECTIONS and self.running:
            new_direction = event.keysym
            if (new_direction == "Up" and self.direction != "Down") or \
               (new_direction == "Down" and self.direction != "Up") or \
               (new_direction == "Left" and self.direction != "Right") or \
               (new_direction == "Right" and self.direction != "Left"):
                self.direction = new_direction

    def move_snake(self):
        """Передвигает змейку на 1 шаг"""
        head_x, head_y = self.snake[0]
        move_x, move_y = DIRECTIONS[self.direction]
        new_head = (head_x + move_x * CELL_SIZE, head_y + move_y * CELL_SIZE)

        # Проверяем столкновение со стенами или собой
        if (
            new_head in self.snake or
            new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT
        ):
            self.running = False
            self.show_game_over()
            return
        
        self.snake.insert(0, new_head)  # Добавляем новую голову

        # Если съели еду, создаем новую и увеличиваем счет
        if new_head == self.food:
            self.food = self.spawn_food()
            self.score += 1
            self.label.config(text=f"Счет: {self.score}")
        else:
            self.snake.pop()  # Убираем хвост

    def draw_elements(self):
        """Рисует змейку и еду"""
        self.canvas.delete("all")
        for segment in self.snake:
            x, y = segment
            self.canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE, fill="green")
        
        fx, fy = self.food
        self.canvas.create_oval(fx, fy, fx + CELL_SIZE, fy + CELL_SIZE, fill="red")

    def show_game_over(self):
        """Отображает сообщение о конце игры и кнопку рестарта"""
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text="Игра окончена", fill="blue", font=("Arial", 20))
        self.start_button.config(text="Начать заново")
        self.start_button.pack()

    def update(self):
        """Обновляет игру"""
        if self.running:
            self.move_snake()
            self.draw_elements()
            self.root.after(SPEED, self.update)  # Перезапускаем цикл игры
        else:
            self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text="Игра окончена", fill="white", font=("Arial", 20))

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()



    