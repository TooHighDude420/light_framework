import sys
import textwrap

from enum import Enum, auto
from pathlib import Path

BASE_DIR = Path(__file__).parent

MODEL_DIR = BASE_DIR / "App" / "Models"
CONTROLLER_DIR = BASE_DIR / "App" / "Controller"
COMPONENT_DIR = BASE_DIR / "App" / "View" / "Component"
VIEW_DIR = BASE_DIR / "App" / "View"
STATIC_DIR = BASE_DIR / "App" / "Statics"

class actions(Enum):
    make = 0
    install = auto()

class targets(Enum):
    model = 0
    view = auto()
    controller = auto()
    component = auto()

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
                    <?php
                    namespace App\\View;

                    class {name}View
                    {{
                        public function show_{name}()
                        {{
                            return "
                                <div>
                                    <p>test</p>
                                </div>
                            ";
                        }}
                    }}""")
                
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
                    <?php
                    namespace App\\View\\Component;

                    class {name}Component
                    {{
                        public function __construct()
                        {{

                        }}
                    }}""")
                
                with open(filename, mode="x") as handle:
                    handle.write(content)

                print(f'component {name} ready to use')

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
        filename = CONTROLLER_DIR / "generalController.php"

        generalContent = textwrap.dedent(f"""\
            <?php
                namespace App\\Controller;

                class GeneralController
                {{
                    public static function linkToAction(string $action)
                    {{
                        return "php/$action.php";
                    }}

                    public static function linkTo(string $location)
                    {{
                        return "index.php?page=$location";
                    }}
                }}
        """)

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
                use App\\Controller\\GeneralController;

                session_start();
                isset($_GET['page']) ? $page = $_GET['page'] : $page = "home";

                $DatabaseController = new DatabaseController();
                $GeneralController = new GeneralController();""")
        
        with open(filename, mode='x') as handle:
            handle.write(indexcont)

        print("install complete")