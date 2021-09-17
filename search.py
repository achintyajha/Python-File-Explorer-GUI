import os
import pickle
import PySimpleGUI as sg
sg.ChangeLookAndFeel('Dark')

class Gui:
    def __init__(self):
        self.layout = [[sg.Text('Search Term', size=(10, 1)), 
                        sg.Input(size=(45, 1), focus=True, key="TERM"), 
                        sg.Radio('Contains', group_id='choice', key="CONTAINS", default=True),
                        sg.Radio('StartsWith', group_id='choice', key="STARTSWITH"), 
                        sg.Radio('EndsWith', group_id='choice', key="ENDSWITH")],
                      [sg.Text('Root Path', size=(10, 1)), 
                        sg.Input('/Users/achintyajha/', size=(45, 1), key="PATH"), 
                        sg.FolderBrowse('Browse'), 
                        sg.Button('Re-Index', size=(10, 1), key="_INDEX_"), 
                        sg.Button('Search', size=(10, 1), bind_return_key=True, key="_SEARCH_")],
                      [sg.Output(size=(100, 30))]]
        self.window = sg.Window('File Search Engine').Layout(self.layout)

class SearchEngine():
    def __init__(self):
        self.file_index= []
        self.results= []
        self.matches = 0
        self.records = 0

    def create_new_index(self, values):
        '''Create a new index and save to file'''
        root_path = values['PATH']
        self.file_index = [(root, files) for root, dirs, files in os.walk(root_path) if files]

        # save to file
        with open('file_index.pkl', 'wb') as f:
            pickle.dump(self.file_index, f)

    def load_existing_index(self):
        '''Load the existing index'''
        try:
            with open('file_index.pkl', 'rb') as f:
                self.file_index = pickle.load(f)
        except:
            self.file_index = []

    def search(self, values):
        '''search for term based on search type'''
        
        # reset variables
        self.results.clear()
        self.matches = 0
        self.records = 0
        term = values['TERM']

        # perform search
        for path, files in self.file_index:
            for file in files:
                self.records += 1
                if (values['CONTAINS'] and term.lower() in file.lower() or
                    values['STARTSWITH'] and file.lower().starts_with(term.lower()) or
                    values['ENDSWITH'] and file.lower().ends_with(term.lower())):

                    result = path.replace('\\', '/') + '/' + file
                    self.results.append(result)
                    self.matches += 1
                else: 
                    continue

        # save search results
        with open('search_results.txt', 'w') as f:
            for row in self.results:
                f.write(row+'\n')

def test1():
    s = SearchEngine()
    s.create_new_index('/Users/achintyajha/')
    s.search('achintya', 'contains')

    print()
    print(f'>> There were {s.matches} matches out of {s.records} records searched.')
    print()
    print(f'>> This query produced the following results: \n')
    for match in s.results:
        print(match)

def test2():
    g = Gui()
    while True:
        event, values = g.window.Read()
        print(event, values)

def main():
    g = Gui()
    s = SearchEngine()
    s.load_existing_index()

    while True:
        event, values = g.window.Read()

        if event is None:
            break
        if event == '_INDEX_':
            s.create_new_index(values)

            print()
            print('>> New Index has been created.')
            print()

        if event == '_SEARCH_':
            s.search(values)

            # print results to output screen
            print()
            for result in s.results:
                print(result)
            
            print()
            print(f'>> There were {s.matches} matches out of {s.records} records searched.')
            print()
            print(f'>> This query produced the following results: \n')
    
main()