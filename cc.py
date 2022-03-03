import enum as Enum
import copy
import csv
filename = './AB_NYC_2019.csv'

"""This is a conversion table the code will use"""
home_currency = ""
conversions = {
        "USD": 1,
        "EUR": 0.9,
        "CAD": 1.4,
        "GBP": 0.8,
        "CHF": 0.95,
        "NZD": 1.66,
        "AUD": 1.62,
        "JPY": 107.92
    }


"""This is the DataSet Class"""


class DataSet:
    header_length = 30

    class EmptyDatasetError(Exception):
        pass

    def __init__(self, header: str):
        self._data = None
        try:
            self._header = header
        except ValueError:
            self._header = ''
        self._labels = {DataSet.Categories.LOCATION: set(),
                        DataSet.Categories.PROPERTY_TYPE: set()}
        self._active_labels = {DataSet.Categories.LOCATION: set(),
                               DataSet.Categories.PROPERTY_TYPE: set()}

    class Categories(Enum.Enum):
        LOCATION = 0
        PROPERTY_TYPE = 1

    class Stats(Enum.Enum):
        MIN = 0
        AVERAGE = 1
        MAX = 2

    def get_labels(self, category: Categories):
        return list(self._labels[category])

    def get_active_labels(self, category: Categories):
        return list(self._active_labels[category])

    @property
    def header(self):
        return self._header

    @header.setter
    def header(self, header_name: str):
        try:
            if len(header_name) > DataSet.header_length:
                raise ValueError
            else:
                self._header = header_name
        except TypeError:
            raise ValueError

    def _initialize_sets(self):
        if not self._data:
            raise DataSet.EmptyDatasetError
        label_list1 = set([item[0] for item in self._data])
        label_list2 = set([item[1] for item in self._data])
        self._labels = {DataSet.Categories.LOCATION: label_list1,
                        DataSet.Categories.PROPERTY_TYPE: label_list2}
        self._active_labels = copy.deepcopy(self._labels)
        return self._labels, self._active_labels

    def _cross_table_statistics(self, descriptor_one:
                                str, descriptor_two: str):
        if not self._data:
            raise DataSet.EmptyDatasetError
        value_list = [item[2] for item in self._data if
                      item[0] == descriptor_one and item[1] == descriptor_two]
        if len(value_list) == 0:
            return None, None, None
        return min(value_list), sum(value_list) / len(value_list), \
            max(value_list)

    def load_default_data(self):
        self._data = [("Staten Island", "Private Room", 70),
                      ("Brooklyn", "Private Room", 50),
                      ("Bronx", "Private Room", 40),
                      ("Brooklyn", "Entire home/apt", 150),
                      ("Manhattan", "Private Room", 125),
                      ("Manhattan", "Entire home/apt", 196),
                      ("Brooklyn", "Private Room", 110),
                      ("Manhattan", "Entire home/apt", 170),
                      ("Manhattan", "Entire home/apt", 165),
                      ("Manhattan", "Entire home/apt", 150),
                      ("Manhattan", "Entire home/apt", 100),
                      ("Brooklyn", "Private Room", 65),
                      ("Queens", "Entire home/apt", 350),
                      ("Manhattan", "Private Room", 99),
                      ("Brooklyn", "Entire home/apt", 200),
                      ("Brooklyn", "Entire home/apt", 150),
                      ("Brooklyn", "Private Room", 99),
                      ("Brooklyn", "Private Room", 120)]
        DataSet._initialize_sets(self)

    def display_cross_table(self, stats: Stats):
        if not self._data:
            raise DataSet.EmptyDatasetError
        print(f"{'':18}", end='')
        for i in self._labels[DataSet.Categories.PROPERTY_TYPE]:
            print(f"{i:18}", end='')
        print()
        for a in self._labels[DataSet.Categories.LOCATION]:
            print(f"{a:18}", end='')
            for b in self._labels[DataSet.Categories.PROPERTY_TYPE]:
                values = self._cross_table_statistics(a, b)[stats.value]
                if values is None:
                    print(f"$ {'N/A':<18}", end="")
                else:
                    print(f"$ {values:<18.2f}", end="")
            print()

    def _alternate_category_type(self, first_category_type):
        """ Given one of the two Category Enum entries, return the
        other one.
        """
        if first_category_type is self.Categories.LOCATION:
            second_category_type = self.Categories.PROPERTY_TYPE
        else:
            second_category_type = self.Categories.LOCATION
        return second_category_type

    def _table_statistics(self, row_category: Categories, label: str):
        if not self._data:
            raise DataSet.EmptyDatasetError
        detail_category = self._alternate_category_type(row_category)
        value_list = [item[2] for item in self._data if
                      item[row_category.value] == label and
                      item[detail_category.value] in
                      self._active_labels[detail_category]]
        if len(value_list) == 0:
            return None, None, None
        return min(value_list), sum(value_list) / len(value_list), \
            max(value_list)

    def toggle_active_label(self, category: Categories, descriptor: str):
        if descriptor in self._labels[category]:
            self._active_labels[category].remove(descriptor)
        if descriptor not in self._labels[category]:
            self._active_labels[category].add(descriptor)
        else:
            raise KeyError

    def display_field_tables(self, rows: Categories):
        if not self._data:
            raise DataSet.EmptyDatasetError
        print("The following data are from properties "
              "matching these criteria:")
        for i in self._active_labels[rows]:
            print(f"- {i}")
        print(f"{'':18}", end='')
        print(f"{'Minimum':18}{'Average':18}{'Maximum':18}")
        for a in self.get_active_labels(rows):
            print(f"{a:18}", end='')
            value = self._table_statistics(rows, a)
            for b in value:
                if value is ():
                    print(f"{'N/A':<18}", end='')
                else:
                    print(f"{b:<18.2f}", end='')
            print()

    def load_data(self):
        """Takes Data from CSV file"""
        file = open(filename, 'r', newline='')
        csvreader = csv.reader(file)
        my_list = [row for row in csvreader]
        for i in range(0, 3):
            del my_list[i]
        my_list = [(i[1], i[2], int(i[3])) for i in my_list]
        self._data = my_list
        DataSet._initialize_sets(self)
        return self._data


def main():
    """Converts input into a name"""
    name = input("Hello, what is your name? ")
    print("Hello " + name + ", welcome.")
    while True:
        choice = input("What is your home currency? ").upper()
        if choice in list(conversions.keys()):
            global home_currency
            home_currency = choice
            break
    while True:
        air_bnb = DataSet("Header")
        try:
            air_bnb.header = input("Please enter a header name. ")
            break
        except ValueError:
            continue
    menu(air_bnb)


"""This will provide a functioning menu"""


def menu(dataset: DataSet):
    """Selects a choice and prints a response based on user input"""
    currency_options(home_currency)
    while True:
        """Keeps running the program repeatedly 
        granted the user does not quit."""
        print(dataset.header)
        print_menu()
        try:
            choice = int(input("Please enter a number between 1 "
                               "and 9 to select a choice: "))
        except ValueError:
            print("Please enter a number; letters are not applicable.")
            print("You will now return to the menu.")
            continue
        if choice == 1:
            print("1 - Print Average Rent by Location and Property Type")
            try:
                dataset.display_cross_table(dataset.Stats.AVERAGE)
            except DataSet.EmptyDatasetError:
                print("Please load data first.")
        elif choice == 2:
            print("2 - Print Minimum Rent by Location and Property Type")
            try:
                dataset.display_cross_table(dataset.Stats.MIN)
            except DataSet.EmptyDatasetError:
                print("Please load data first.")
        elif choice == 3:
            print("3 - Print Maximum Rent by Location and Property Type")
            try:
                dataset.display_cross_table(dataset.Stats.MAX)
            except DataSet.EmptyDatasetError:
                print("Please load data first.")
        elif choice == 4:
            print("4 - Print Min/Avg/Max by Location")
            try:
                dataset.display_field_tables(dataset.Categories.LOCATION)
            except dataset.EmptyDatasetError:
                print("Please load data first.")
        elif choice == 5:
            print("5 - Print Min/Avg/Max by Property Type")
            try:
                dataset.display_field_tables(dataset.Categories.
                                             PROPERTY_TYPE)
            except dataset.EmptyDatasetError:
                print("Please load data first.")
        elif choice == 6:
            print("6 - Adjust Location Filters")
            try:
                manage_filters(dataset, dataset.Categories.LOCATION)
            except DataSet.EmptyDatasetError:
                print("Please load data first.")
        elif choice == 7:
            print("7 - Adjust Property Type Filters")
            try:
                manage_filters(dataset, dataset.Categories.PROPERTY_TYPE)
            except DataSet.EmptyDatasetError:
                print("Please load data first.")
        elif choice == 8:
            DataSet.load_data(dataset)
            print("8 - Load Data")
        elif choice == 9:
            print("9 - Quit")
            break
        else:
            print("Please enter a valid number.")
        print("You will now return to the menu.")
    print("Thank you for visiting.")


"""Provides a menu within the main function"""


def print_menu():
    """Prints the menu for the user"""
    print("Main Menu")
    print("1 - Print Average Rent by Location and Property Type")
    print("2 - Print Minimum Rent by Location and Property Type")
    print("3 - Print Maximum Rent by Location and Property Type")
    print("4 - Print Min/Avg/Max by Location")
    print("5 - Print Min/Avg/Max by Property Type")
    print("6 - Adjust Location Filters")
    print("7 - Adjust Property Type Filters")
    print("8 - Load Data")
    print("9 - Quit")


def currency_converter(quantity: float, source_curr: str, target_curr: str):
    """Contains formula to convert currency"""
    if quantity == 0:
        raise ValueError
    total = quantity / conversions[source_curr] * (conversions[target_curr])
    return total


def currency_options(base_curr='EUR'):
    """This prints the currency table with the conversions"""
    print(f"Options for converting from {home_currency}:")
    for i in conversions:
        print(f"{i:8}", end="")
    print()
    for x in range(10, 100, 10):
        for i in conversions:
            y = currency_converter(x, base_curr, i)
            print(f"{y:<8.2f}", end='')
        print()
    return base_curr


def manage_filters(dataset: DataSet, category: DataSet.Categories):
    print("The following labels are in the dataset: ")
    while True:
        for n, i in enumerate(dataset.get_labels(category), 1):
            if i in dataset.get_active_labels(category):
                print(f"{n}. {i:18} Active")
            elif i not in dataset.get_active_labels(category):
                print(f"{n}. {i:18} Inactive")
        choices = input("Please select an item to toggle or "
                        "enter a blank line when you are finished: ")
        if choices == "":
            break
        else:
            choices = int(choices)
            labels = dataset.get_labels(category)
            dataset.toggle_active_label(category, labels[choices - 1])


if __name__ == "__main__":
    main()

