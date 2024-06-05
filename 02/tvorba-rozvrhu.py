import json
import random
import os
from datetime import datetime
from fpdf import FPDF

# Funkce pro načtení JSON souboru
def load_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)

# Funkce pro výběr souboru ze složky input
def select_input_file():
    files = os.listdir('input')
    json_files = [f for f in files if f.endswith('.json')]
    if not json_files:
        print("Ve složce input se nenachází parametrický .json soubor. Vložte ho prosím.")
        return None
    
    print("Prosím vyberte parametrický soubor:")
    for idx, file in enumerate(json_files, 1):
        print(f"{idx}: {file}")
    
    while True:
        try:
            choice = int(input("Zadejte prosím číslo parametrického souboru pro který chcete vytvořit rozvrh: "))
            if 1 <= choice <= len(json_files):
                return os.path.join('input', json_files[choice - 1])
            else:
                print("Neplatná selekce, zadejte prosím znovu.")
        except ValueError:
            print("Neplatný vstup, zadejte číslo prosím.")

# Funkce pro generování rozvrhu
def generate_schedule(data):
    print("Generování rozvrhu...")
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    time_slots = [f'{hour}:00-{hour+1}:00' for hour in range(8, 17)]
    schedule = {class_info['name']: {day: [None]*len(time_slots) for day in days} for class_info in data['classes']}
    
    teacher_availability = {teacher['name']: {day: [True]*len(time_slots) for day in days} for teacher in data['teachers']}
    
    class_subjects = {class_info['name']: class_info['subjects'] for class_info in data['classes']}
    room_types = {room['type']: [] for room in data['rooms']}
    for room in data['rooms']:
        room_types[room['type']].append(room['name'])
    
    def assign_hour(class_name, day, slot, subject, teacher, room):
        schedule[class_name][day][slot] = {
            'subject': subject['name'],
            'teacher': teacher['name'],
            'room': room
        }
        teacher_availability[teacher['name']][day][slot] = False

    for class_name, subjects in class_subjects.items():
        print(f"Plánování rozvrhu fixně pro ranní hodiny pro třídu {class_name}...")
        for day in days:
            for slot in range(4):  # Fixed slots for 8:00 to 11:40
                subject = next((s for s in subjects if s['hours'] > 0), None)
                if subject is None:
                    break
                
                available_teachers = [teacher for teacher in data['teachers'] if subject['name'] in teacher['subjects']]
                if not available_teachers:
                    print(f"Není volný učitel pro tento předmet {subject['name']} ve tříde {class_name}")
                    return None
                teacher = random.choice(available_teachers)
                
                room_type = 'kmenová'
                if subject['name'] in ['INF', 'PROG']:
                    room_type = 'PC'
                elif subject['name'] in ['ANG']:
                    room_type = 'jazyková'
                elif subject['name'] in ['TV']:
                    room_type = 'tělocvična'
                elif subject['name'] in ['STRO', 'DIL']:
                    room_type = 'dílna'
                
                available_rooms = room_types.get(room_type, [])
                if available_rooms:
                    room = random.choice(available_rooms)
                    assign_hour(class_name, day, slot, subject, teacher, room)
                    subject['hours'] -= 1
                else:
                    print(f"Není dostupná místnost pro předmět {subject['name']} ve třídě {class_name} v {day} v {time_slots[slot]}")
                    return None
    
    for class_name, subjects in class_subjects.items():
        print(f"Generování zbylých hodin pro třídu {class_name}...")
        for subject in subjects:
            hours_to_assign = subject['hours']
            attempts = 0
            max_attempts = 1000  # Limit the number of attempts to avoid infinite loops
            while hours_to_assign > 0:
                if attempts > max_attempts:
                    print(f"Error: nemožno vytvořit rozvrh s předmětem {subject['name']} pro třídu {class_name}.")
                    return None
                day = random.choice(days)
                slot = random.choice(range(4, len(time_slots)))  # Start scheduling from 12:00
                
                if schedule[class_name][day][slot] is None:
                    available_teachers = [teacher for teacher in data['teachers'] if subject['name'] in teacher['subjects']]
                    if not available_teachers:
                        raise ValueError(f"Není volný učitel pro tento předmět {subject['name']} ve třídě {class_name}")
                    teacher = random.choice(available_teachers)
                    if teacher_availability[teacher['name']][day][slot]:
                        room_type = 'kmenová'
                        if subject['name'] in ['INF', 'PROG']:
                            room_type = 'PC'
                        elif subject['name'] in ['ANG']:
                            room_type = 'jazyková'
                        elif subject['name'] in ['TV']:
                            room_type = 'tělocvična'
                        elif subject['name'] in ['STRO', 'DIL']:
                            room_type = 'dílna'
                        
                        available_rooms = room_types.get(room_type, [])
                        if available_rooms:
                            room = random.choice(available_rooms)
                            assign_hour(class_name, day, slot, subject, teacher, room)
                            hours_to_assign -= 1
                        else:
                            print(f"Není volná místnost pro předmět {subject['name']} ve třídě {class_name} v {day} v {time_slots[slot]}")
                    attempts += 1
    
    print("Generování rozvrhu dokončeno.")
    return schedule

# Funkce pro generování PDF - vytvořeno za pomoci ChatGPT
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'School Schedule', 0, 1, 'C')
        self.ln(10)
    
    def chapter_title(self, class_name):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, f'Class {class_name}', 0, 1, 'L')
        self.ln(5)

    def chapter_body(self, schedule, class_name, time_slots):
        self.set_font('Arial', '', 10)
        for day, subjects in schedule.items():
            self.cell(0, 10, day, 0, 1, 'L')
            for slot, subject in enumerate(subjects):
                if subject:
                    self.cell(0, 10, f'{time_slots[slot]}: {subject["subject"]} with {subject["teacher"]} in {subject["room"]}', 0, 1, 'L')
                else:
                    self.cell(0, 10, f'{time_slots[slot]}: Free', 0, 1, 'L')
            self.ln(5)
    
    def add_class_schedule(self, schedule, class_name, time_slots):
        self.add_page()
        self.chapter_title(class_name)
        self.chapter_body(schedule[class_name], class_name, time_slots)

    def chapter_table(self, schedule, class_name, days, time_slots):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, f'Class {class_name}', 0, 1, 'L')
        self.ln(5)
        self.set_font('Arial', 'B', 10)
        self.cell(20, 10, '', 1)
        for day in days:
            self.cell(25, 10, day, 1)
        self.ln()
        self.set_font('Arial', '', 10)
        for slot, time in enumerate(time_slots):
            self.cell(20, 10, time, 1)
            for day in days:
                subject = schedule[class_name][day][slot]
                if subject:
                    self.cell(25, 10, f'{subject["subject"]}\n{subject["teacher"]}\n{subject["room"]}', 1)
                else:
                    self.cell(25, 10, '', 1)
            self.ln()
        self.ln(5)
    
    def add_class_table(self, schedule, class_name, days, time_slots):
        self.add_page()
        self.chapter_table(schedule, class_name, days, time_slots)

def create_pdf(schedule, filename):
    if schedule is None:
        print("Failed to generate the schedule. No PDF will be created.")
        return
    pdf = PDF()
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    time_slots = [f'{hour}:00-{hour+1}:00' for hour in range(8, 17)]
    
    for class_name in schedule.keys():
        pdf.add_class_table(schedule, class_name, days, time_slots)
    
    pdf.output(filename)
    print(f"PDF saved as {filename}")

# Hlavní část programu
def main():
    input_file = select_input_file()
    if input_file is None:
        return
    
    data = load_data(input_file)
    schedule = generate_schedule(data)
    
    # Vytvořit složku output, pokud neexistuje
    if not os.path.exists('output'):
        os.makedirs('output')

    # Vygenerovat unikátní název souboru
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'output/schedule_{timestamp}.pdf'
    
    create_pdf(schedule, filename)

if __name__ == '__main__':
    main()
