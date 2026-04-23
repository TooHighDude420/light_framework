import os
import sys
import textwrap
import shutil

import numpy as np

from datetime import datetime
from enum import Enum, auto
from pathlib import Path
from dotenv import load_dotenv
from mysql.connector import connect
from rich.console import Console

BASE_DIR = Path(__file__).parent

load_dotenv(BASE_DIR / ".env")

MODEL_DIR = BASE_DIR / "App" / "Models"
CONTROLLER_DIR = BASE_DIR / "App" / "Controller"
COMPONENT_DIR = BASE_DIR / "App" / "View" / "Component"
VIEW_DIR = BASE_DIR / "App" / "View"
STATIC_DIR = BASE_DIR / "App" / "Statics"
OUTPUT_DIR = BASE_DIR / "Maker_Out"
SQL_DIR = OUTPUT_DIR / "SQL"
BACKUP_LAYOUT_DIR = SQL_DIR / "History"

DATABASE_LAYOUTFILE = "DataBaseLayout"
BACKUP_LAYOUTFILE = "__DataBaseLayout"


DATABASE = os.getenv("DB_DATABASE")

console = Console(color_system="truecolor")

class actions(Enum):
    make = 0
    install = auto()
    migration = auto()
    drop = auto()

class targets(Enum):
    model = 0
    view = auto()
    controller = auto()
    component = auto()
    table = auto()

def in_table(col, tableres):
    in_table = False

    if not in_table:
        for r in tableres:
            if not in_table:
                if r[0] in col:
                    in_table = True
                    break
            else:
                break

    return in_table

match len(sys.argv):
    case 2:
        do = sys.argv[1]

    case 3:
        action = sys.argv[1].lower()

        actiontarget = action.split(':')

        do = actiontarget[0]
        target = actiontarget[1]
        name = sys.argv[2]

match do:
    case actions.drop.name:
        match target:
            case targets.table.name:
                databaseconn = connect(
                    host="127.0.0.1",
                    user=os.getenv("DB_USERNAME"),
                    password=os.getenv("DB_PASSWORD"),
                    database=DATABASE
                )

                databaseconn.autocommit = True

                cursor = databaseconn.cursor()

                sql = f"DROP TABLE {DATABASE}.{name}"
                
                conf = input(f'are you shure this will delete {DATABASE}.{name} y/n:\n')

                match conf:
                    case 'y':
                        cursor.execute(sql)
                        os.remove(SQL_DIR / f"{DATABASE_LAYOUTFILE}{name}.sql")
                        # shutil.rmtree(SQL_DIR / f"{DATABASE_LAYOUTFILE}{name}.sql")
                        console.log(f"removed {DATABASE}.{name}")
                    case 'n':
                        sys.exit()

    case actions.make.name:
        match target:
            case targets.model.name:
                if not (MODEL_DIR.exists()):
                    MODEL_DIR.mkdir(parents=True, exist_ok=True)

                filename = f"{MODEL_DIR / name}.php"

                content = textwrap.dedent(f"""\
                    <?php
                    namespace App\\Models;

                    class {name}
                    {{
                        //paramaters go here
                        public string $example;

                        public function __construct(string $example)
                        {{
                            //construction goes here
                            $this->example = $example;
                        }}
                    }}""")
                
                with open(filename, mode="x") as handle:
                    handle.write(content)

                print(f'model {name} ready for use')
                
            case targets.view.name:
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
            
            case targets.controller.name:
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
            
            case targets.component.name:
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

            case targets.table.name:
                databaseconn = connect(
                    host="127.0.0.1",
                    user=os.getenv("DB_USERNAME"),
                    password=os.getenv("DB_PASSWORD"),
                    database=DATABASE
                )

                databaseconn.autocommit = True

                cursor = databaseconn.cursor()
                
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

    case actions.install.name:
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

        # build generic databasecontroller
        filename = CONTROLLER_DIR / "databaseController.php"

        databasecontent = textwrap.dedent(f"""\
            <?php
                namespace App\\Controller;
                use App\\Models\\User;
                use App\\Statics\\DatabaseSingleton;

                use PDO, PDOException;
                use UnexpectedValueException;
                use ValueError;

                enum DatabaseActions{{
                    case SELECT;
                    case INSERT;
                    case UPDATE;
                    case DELETE;
                }}


                class DatabaseController
                {{
                    private $Conn;

                    public function __construct()
                    {{
                        DatabaseSingleton::$conn ?: DatabaseSingleton::makeCon();
                        $this->Conn = DatabaseSingleton::$conn;
                    }}

                    public function getFromTable(string $table, bool $all, bool $where, ?string $condition = null, ?array $columns = null): array
                    {{
                        if ($all) {{
                            $sql = "SELECT * FROM $table";
                        }} else {{
                            $sql = "SELECT";

                            if (count($columns) > 1) {{
                                foreach ($columns as $column) {{
                                    $sql .= " $column,";
                                    print ($sql);
                                }}
                            }} else {{
                                $sql .= " $columns[0]";
                            }}

                            $sql .= " FROM $table";
                        }}

                        if ($where) {{
                            $sql .= " WHERE $condition";
                        }}

                        $stmt = $this->Conn->prepare($sql);
                        $stmt->execute();

                        return $stmt->fetchAll();
                    }}

                    public function test(DatabaseActions $action, string $table, ?array $columns = null, ?array $values): null | array{{
                        switch ($action) {{
                            case DatabaseActions::INSERT:
                                if ($columns){{
                                    $sql = "INSERT ";

                                    foreach ($columns as $col){{
                                        $sql .= $col;
                                        $sql .= ", ";
                                    }}
                                }}

                                return null;

                            case DatabaseActions::SELECT:
                                return [];
                            
                            case DatabaseActions::UPDATE:
                                return null;

                            case DatabaseActions::DELETE:
                                return null;

                            default:
                                throw new ValueError("wtf bro");
                        }}
                    }}
                }}""")
        
        with open(filename, mode='x') as handle:
            handle.write(databasecontent)

        # build generalController
        filename = STATIC_DIR / "route.php"

        generalContent = textwrap.dedent(r"""<?php
namespace App\Statics;
use ValueError;

class Route
{
    private static $routes = [];

    public static function linkToAction(string $action)
    {
        return "php/$action.php";
    }

    public static function linkTo(string $location)
    {
        return "/$location";
    }

    public static function register_route(string $routename, string $viewname){
        if(isset(Route::$routes[$routename])){
            throw new ValueError("$routename already exists");
        } else {
            Route::$routes[$routename] = $viewname;
        }
    }

    public static function register_routes(array $routes){
        foreach ($routes as $key => $val){
            Route::register_route($key, $val);
        }
    }

    public static function get_uri(){
        if (isset(Route::$routes[$_SERVER['REQUEST_URI']])){
            $selector = Route::$routes[$_SERVER['REQUEST_URI']];
            return $selector;
        } else {
            throw new ValueError("Route not registerd or not found");
        }
    }

    public static function render(string $url): mixed {
        return include "App/View/$url.inc.php";
    }

    public static function render_component(string $name, $data){            
        extract($data);

        return include "App/View/Component/$name.comp.php";
    }
}""")

        with open(filename, mode='x') as handle:
            handle.write(generalContent)

        # build databaseSingleton

        filename = STATIC_DIR / "databaseSingleton.php"

        singletonContent = textwrap.dedent(f"""\
            <?php
                namespace App\\Statics;
                use PDO, PDOException;

                class DatabaseSingleton
                {{
                    public static ?PDO $conn = null;

                    public static function makeCon() :void
                    {{
                        if (DatabaseSingleton::$conn == false) {{
                            $servername = "db";
                            $username = "root";
                            $password = getenv('DB_ROOT_PASSWORD');
                            $dbname = getenv('DB_DATABASE');

                            try {{
                                DatabaseSingleton::$conn = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
                                DatabaseSingleton::$conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
                            }} catch (PDOException $e) {{
                                echo "Connection failed: " . $e->getMessage();
                            }}
                        }}
                    }}

                    public static function closeCon(){{
                        DatabaseSingleton::$conn = null;
                    }}
                }}
        """)

        with open(filename, mode='x') as handle:
            handle.write(singletonContent)

        # build autoloader

        filename = BASE_DIR / "AutoLoad.php"

        autocontent = textwrap.dedent(f"""\
            <?php
                spl_autoload_register(function ($class) {{
                    $baseDir = __DIR__ . '/';

                    $file = $baseDir . str_replace('\\\\', '/', $class) . '.php';

                    if (file_exists($file)) {{
                        require $file;
                    }} else {{
                        echo "Class file not found: $file\\n";
                    }}
                }});""")
        
        with open(filename, mode='x') as handle:
            handle.write(autocontent)

        #example index

        filename = BASE_DIR / "index.php"

        indexcont = textwrap.dedent(f"""\
            <?php
                require_once("AutoLoad.php");

                use App\\Controller\\DatabaseController;
                use App\\Statics\\Route;

                session_start();
                isset($_GET['page']) ? $page = $_GET['page'] : $page = "home";

                $DatabaseController = new DatabaseController();
                                    
                Route::register_routes([
                    "/" => "home",
                    "/projects" => "projects",
                    "/about", "about"
                ]);

                $request = Route::get_uri();
                                """)
        
        with open(filename, mode='x') as handle:
            handle.write(indexcont)

        print("install complete")

    case actions.migration.name:
        databaseconn = connect(
            host="127.0.0.1",
            user=os.getenv("DB_USERNAME"),
            password=os.getenv("DB_PASSWORD"),
            database=DATABASE
        )

        databaseconn.autocommit = True

        cursor = databaseconn.cursor()

        for database_file in SQL_DIR.iterdir():
            if database_file.is_file():
                name = database_file.stem.replace(DATABASE_LAYOUTFILE, "")

                with open(database_file, mode='r') as input:
                    deltacont = input.read()

                latest = max((BACKUP_LAYOUT_DIR / name).iterdir(), key=lambda p: p.name)

                with open(latest, mode='r') as current:
                    latestcont = current.read()

                latestcont = latestcont.strip()
                latestcont = latestcont.split(',') 

                deltacont = deltacont.strip()
                deltacont = deltacont.split(',')

                for cont in deltacont:
                    i = deltacont.index(cont)
                    deltacont[i] = cont.strip()

                for lat in latestcont:
                    i = latestcont.index(lat)
                    latestcont[i] = lat.strip()

                latestarray = np.array(latestcont)
                deltarray = np.array(deltacont)

                if not np.array_equal(latestarray, deltarray):
                    missing_in_delta = np.setdiff1d(latestarray, deltarray)
                    extra_in_delta   = np.setdiff1d(deltarray, latestarray)
                    
                    update_his = False

                    if len(extra_in_delta) > 0:
                        update_his = True

                        for extra in extra_in_delta:
                            sql = f"ALTER TABLE {DATABASE}.{name} ADD "
                            stmt = sql + extra
                            cursor.execute(stmt)

                            field = str(extra).split(' ')[0]
                            console.log(f"added {field} to {DATABASE}.{name}")
                    
                    if len(missing_in_delta) > 0:
                        update_his = True

                        for missing in missing_in_delta:
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