<?php
    namespace App\Controller;
    use App\Models\User;
    use App\Statics\DatabaseSingleton;

    use PDO, PDOException;
    use UnexpectedValueException;
    use ValueError;

    enum DatabaseActions{
        case SELECT;
        case INSERT;
        case UPDATE;
        case DELETE;
    }


    class DatabaseController
    {
        private PDO $Conn;

        public function __construct()
        {
            DatabaseSingleton::$conn ?: DatabaseSingleton::makeCon();
            $this->Conn = DatabaseSingleton::$conn;
        }

        public function getFromTable(string $table, bool $all, bool $where, ?string $condition = null, ?array $columns = null): array
        {
            if ($all) {
                $sql = "SELECT * FROM $table";
            } else {
                $sql = "SELECT";

                if (count($columns) > 1) {
                    foreach ($columns as $column) {
                        $sql .= " $column,";
                        print ($sql);
                    }
                } else {
                    $sql .= " $columns[0]";
                }

                $sql .= " FROM $table";
            }

            if ($where) {
                $sql .= " WHERE $condition";
            }

            $stmt = $this->Conn->prepare($sql);
            $stmt->execute();

            return $stmt->fetchAll();
        }

        public function test(DatabaseActions $action, string $table, ?array $columns = null, ?array $values = null): null | array{
            switch ($action) {
                case DatabaseActions::INSERT:
                    if ($columns){
                        $sql = "INSERT ";

                        foreach ($columns as $col){
                            $sql .= $col;
                            $sql .= ", ";
                        }
                    }

                    return null;

                case DatabaseActions::SELECT:
                    return [];

                case DatabaseActions::UPDATE:
                    return null;

                case DatabaseActions::DELETE:
                    return null;

                default:
                    throw new ValueError("wtf bro");
            }
        }
    }