import os
import sys
import textwrap
import shutil
# import argparse

import numpy as np

from datetime import datetime
from enum import Enum, auto
from pathlib import Path
from dotenv import load_dotenv
from mysql.connector import connect
from rich.console import Console
from rich.table import Table

BASE_DIR = Path(__file__).parent

# IMPORTANT TODOS:
# phase migrations
# work out deps
# reintergrate files for one file download framework
# intergrate argparser
# extend readme
# parser = argparse.ArgumentParser(prog="orchestrator")

load_dotenv(BASE_DIR / ".env")

# needed folder constants and filename constants
MODEL_DIR = BASE_DIR / "App" / "Models"
CONTROLLER_DIR = BASE_DIR / "App" / "Controller"
BASECLASSES_DIR = BASE_DIR / "App" / "Baseclasses"
COMPONENT_DIR = BASE_DIR / "App" / "View" / "Component"
VIEW_DIR = BASE_DIR / "App" / "View"
STATIC_DIR = BASE_DIR / "App" / "Statics"
TEMPLATE_DIR = BASE_DIR / "Basefiles"
OUTPUT_DIR = BASE_DIR / "Maker_Out"
SQL_DIR = OUTPUT_DIR / "SQL"
BACKUP_LAYOUT_DIR = SQL_DIR / "History"

DATABASE_LAYOUTFILE = "DataBaseLayout"
BACKUP_LAYOUTFILE = "__DataBaseLayout"

DATABASE = os.getenv("DB_DATABASE")

# all available actions
class actions(Enum):
    make = 0
    install = auto()
    migration = auto()
    drop = auto()
    show = auto()

# all available targets
class targets(Enum):
    model = 0
    view = auto()
    controller = auto()
    component = auto()
    table = auto()

def makeCon(databaseconn):
    if databaseconn != None:
        return
    
    databaseconn = connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
        database=DATABASE
    )

    return databaseconn

# drop functions
def drop_table(cursor, name:str):
    sql = f"DROP TABLE {DATABASE}.{name}"
    cursor.execute(sql)
    os.remove(SQL_DIR / f"{DATABASE_LAYOUTFILE}{name}.sql")
    console.log(f"removed {DATABASE}.{name}")

# make functions
def make_model(name:str):
    if not (MODEL_DIR.exists()):
        MODEL_DIR.mkdir(parents=True, exist_ok=True)

    filename = f"{MODEL_DIR / name}.php"

    content = textwrap.dedent(rf"""<?php
namespace App\Models;
use App\Baseclasses\Models;

class {name} extends Models
{{

}}
""")
                
    with open(filename, mode="x") as handle:
        handle.write(content)

    print(f'model {name} ready for use')

def make_view(name:str):
    if not (VIEW_DIR.exists()):
        VIEW_DIR.mkdir(parents=True, exist_ok=True)

    filename = f"{VIEW_DIR / name}.inc.php"

    content = textwrap.dedent(f"""\
        <div>
            <p><!--sometimes it be always--></p>
        </div>""")
    
    with open(filename, mode="x") as handle:
        handle.write(content)

    print(f'view {name} ready for use')

def make_controller(name:str):
    if not (CONTROLLER_DIR.exists()):
        CONTROLLER_DIR.mkdir(parents=True, exist_ok=True)

    filename = f"{CONTROLLER_DIR / name}Controller.php"

    content = textwrap.dedent(f"""\
        <?php
        namespace App\\Controller;

        class {name}Controller
        {{
            public function __construct()
            {{

            }}
        }}""")
    
    with open(filename, mode="x") as handle:
        handle.write(content)

    print(f'controller {name} ready for use')

def make_component(name: str):
    if not (COMPONENT_DIR.exists()):
        COMPONENT_DIR.mkdir(parents=True, exist_ok=True)

    filename = f"{COMPONENT_DIR / name}.comp.php"

    content = textwrap.dedent(f"""\
        <div>
        
        </div>    
    """)
    
    with open(filename, mode="x") as handle:
        handle.write(content)

    print(f'component {name} ready to use')

def make_table(name:str, cursor):
    sql = textwrap.dedent(f"""\
        CREATE TABLE IF NOT EXISTS {DATABASE}.{name}(
            {name}ID INT PRIMARY KEY auto_increment NOT NULL          
        );
    """)

    cursor.execute(sql)

    if not SQL_DIR.exists():
        SQL_DIR.mkdir(parents=True, exist_ok=True)

    if not (BACKUP_LAYOUT_DIR / name).exists():
        (BACKUP_LAYOUT_DIR / name).mkdir(parents=True, exist_ok=True)

    with open(SQL_DIR / f"{DATABASE_LAYOUTFILE}{name}.sql", mode='w') as handle:
        handle.write(f"{name}ID INT PRIMARY KEY auto_increment NOT NULL")

    shutil.copy(SQL_DIR / f"{DATABASE_LAYOUTFILE}{name}.sql", BACKUP_LAYOUT_DIR / name / f"000{BACKUP_LAYOUTFILE}{name}.sql")

    console.log(f"made table {name}")

# installation functions
def install():
    if not MODEL_DIR.exists():
            MODEL_DIR.mkdir(parents=True, exist_ok=True)

    if not CONTROLLER_DIR.exists():
        CONTROLLER_DIR.mkdir(parents=True, exist_ok=True)

    if not COMPONENT_DIR.exists():
        COMPONENT_DIR.mkdir(parents=True, exist_ok=True)

    if not VIEW_DIR.exists():
        VIEW_DIR.mkdir(parents=True, exist_ok=True)

    if not STATIC_DIR.exists():
        STATIC_DIR.mkdir(parents=True, exist_ok=True)

    if not BASECLASSES_DIR.exists():
        BASECLASSES_DIR.mkdir(exist_ok=True, parents=True)

    # build generic databasecontroller
    filename = CONTROLLER_DIR / "databaseController.php"

    databasecontent = open(TEMPLATE_DIR / "database_controller_template.php", mode='r').read()
    
    with open(filename, mode='x') as handle:
        handle.write(databasecontent)

    # build generalController
    filename = STATIC_DIR / "route.php"

    generalContent = open(TEMPLATE_DIR / "route_template.php", mode='r').read()

    with open(filename, mode='x') as handle:
        handle.write(generalContent)

    # build databaseSingleton

    filename = STATIC_DIR / "databaseSingleton.php"

    singletonContent = open(TEMPLATE_DIR / "database_singleton_template.php", mode='r').read()

    with open(filename, mode='x') as handle:
        handle.write(singletonContent)

    # build autoloader

    filename = BASE_DIR / "AutoLoad.php"

    autocontent = open(TEMPLATE_DIR / "autoload_template.php", mode='r').read()
    
    with open(filename, mode='x') as handle:
        handle.write(autocontent)

    #example index
    filename = BASE_DIR / "index.php"

    indexcont = open(TEMPLATE_DIR / "template_index.php", mode='r').read()
    
    with open(filename, mode='x') as handle:
        handle.write(indexcont)

    # make model baseclass
    filename = BASECLASSES_DIR / "Models.php"

    modlescont = open(TEMPLATE_DIR / "models_template.php", mode='r').read()

    with open(filename, mode='x') as handle:
        handle.write(modlescont)

    print("install complete")

# migrations functions
def sql_parsing(database_file):
    phase_one:list[str] = []
    phase_two:list[str] = []
    phase = ""

    with open(database_file, "r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            stripped = line.strip()

            # Empty line
            if not stripped:
                continue

            # Single-line SQL comment
            if stripped.startswith("--"):
                if "one" in stripped:
                    phase = "one"
                elif "two" in stripped:
                    phase = "two"
                
                continue

            match phase:
                case "one":
                    if "\n" in line:
                        line = line.replace("\n", "")

                    phase_one.append(line)

                case "two":
                    if "\n" in line:
                        line = line.replace("\n", "")
                    
                    phase_two.append(line)

                case _:
                    raise ValueError(f"this should not happen, input: phase:{phase}, line:{line}, file:{database_file} line:286")
            
    return (phase_one, phase_two)
        
def migration(cursor):
    for database_file in SQL_DIR.iterdir():
        if database_file.is_file():
            phase_one, phase_two = sql_parsing(database_file)
            name = database_file.stem.replace(DATABASE_LAYOUTFILE, "")

            deltarray = (np.array(phase_one), np.array(phase_two))
            
            if (BACKUP_LAYOUT_DIR / name).exists():
                latest = max((BACKUP_LAYOUT_DIR / name).iterdir(), key=lambda p: p.name)

                latest_one, latest_two = sql_parsing(latest)

                latestarray = (np.array(latest_one), np.array(latest_two))
                
                same = (
                    np.array_equal(latestarray[0], deltarray[0])
                    and
                    np.array_equal(latestarray[1], deltarray[1])
                )

                if not same:
                    missing_in_phase_one = np.setdiff1d(latestarray[0], deltarray[0])
                    missing_in_phase_two = np.setdiff1d(latestarray[1], deltarray[1])
                    
                    extra_in_phase_one = np.setdiff1d(deltarray[0], latestarray[0])                   
                    extra_in_phase_two = np.setdiff1d(deltarray[1], latestarray[1])                   
                
                    update_his = False

                    if len(extra_in_phase_one) > 0:
                        update_his = True

                        for extra in extra_in_phase_one:
                            sql = f"ALTER TABLE {DATABASE}.{name} ADD "
                            stmt = sql + extra
                            cursor.execute(stmt)

                            field = str(extra).split(' ')[0]
                            console.log(f"added {field} to {DATABASE}.{name}")
                    
                    if len(extra_in_phase_two)  > 0:
                        update_his = True

                        for extra in extra_in_phase_two:
                            sql = f"ALTER TABLE {DATABASE}.{name} "
                            stmt = sql + extra
                            cursor.execute(stmt)

                            con_name = str(extra).split(' ')[2]
                            console.log(f"added {con_name} to {DATABASE}.{name}")
                    
                    if len(missing_in_phase_one) > 0:
                        update_his = True

                        for missing in missing_in_phase_one:
                            sql = f"ALTER TABLE {DATABASE}.{name} DROP COLUMN "
                            field = str(missing).split(' ')[0]
                            stmt = sql + field
                            cursor.execute(stmt)
                            console.log(f"removed {field} from {DATABASE}.{name}")

                    if update_his:
                        num = latest.stem.split('__')[0]
                        num = int(num)
                        num += 1
                        num = f"{num:03d}"

                        shutil.copy(SQL_DIR / f"{DATABASE_LAYOUTFILE}{name}.sql", BACKUP_LAYOUT_DIR / name / f"{num}{BACKUP_LAYOUTFILE}{name}.sql")

                else:
                    console.log(f"nothing to migrate for {name}")

            else:
                sql = f"CREATE TABLE IF NOT EXISTS {name} (\n"
                sql += ",\n".join(phase_one)
                sql += "\n);\n"

                cursor.execute(sql)

                if len(phase_two) > 0:
                    for cons in phase_two:
                        sql = f"ALTER TABLE {DATABASE}.{name} "
                        stmt = sql + cons
                        cursor.execute(stmt)
                
                if not (BACKUP_LAYOUT_DIR / name).exists():
                    (BACKUP_LAYOUT_DIR / name).mkdir(parents=True, exist_ok=True)

                shutil.copy(SQL_DIR / f"{DATABASE_LAYOUTFILE}{name}.sql", BACKUP_LAYOUT_DIR / name / f"000{BACKUP_LAYOUTFILE}{name}.sql")
                console.log(f"{name} history not detected, made table {name}")

# display database functions
def display_all(cursor):
    sql = f"SHOW TABLES"

    cursor.execute(sql)

    res = cursor.fetchall()

    table = Table("database name", title=f"{DATABASE}.{name}")

    for tables in res:
        table.add_row(tables[0])

    console.print(table)

def display_table(name, cursor):
    sql = f"DESCRIBE {DATABASE}.{name}"

    cursor.execute(sql)

    res = cursor.fetchall()
    
    columns = []

    for column in res:
        columns.append(column[0])

    table = Table(*columns, title=f"{DATABASE}.{name}")

    sql = f"SELECT * FROM {DATABASE}.{name}"
    cursor.execute(sql)

    res = cursor.fetchall()

    for row in res:
        table.add_row(*row)

    console.print(table)

do = ""
target = ""
name = ""
cursor = None
databaseconn = None
console = Console(color_system="truecolor")
args = sys.argv

match len(sys.argv):
    case 2:
        do = sys.argv[1]

    case 3:
        action = sys.argv[1].lower()

        actiontarget = action.split(':')

        do = actiontarget[0]
        target = actiontarget[1]
        name = sys.argv[2]

if do == None:
    console.log("please enter something")
    sys.exit()

if databaseconn == None:
    databaseconn = makeCon(databaseconn)
    if databaseconn != None:
        cursor = databaseconn.cursor()

match do:
    case actions.drop.name:
        match target:
            case targets.table.name:
                conf = input(f'are you shure this will delete {DATABASE}.{name} y/n:\n')

                match conf:
                    case 'y':
                        drop_table(cursor, name)
                    case 'n':
                        sys.exit()

    case actions.make.name:
        match target:
            case targets.model.name:
                make_model(name)
                
            case targets.view.name:
                make_view(name)
                
            case targets.controller.name:
                make_controller(name)

            case targets.component.name:
                make_component(name)

            case targets.table.name:
                make_table(name, cursor)

    case actions.install.name:
        install()
        
    case actions.migration.name:
        migration(cursor)

    case actions.show.name:
        match target:
            case targets.table.name:
                match name:
                    case 'all':
                        display_all(cursor)
                    
                    case _:
                        display_table(name, cursor)