<?php
    namespace App\Statics;
    use PDO, PDOException;

    class DatabaseSingleton
    {
        public static ?PDO $conn = null;

        public static function makeCon() :void
        {
            if (DatabaseSingleton::$conn == false) {
                $servername = getenv('DB_HOST');
                $username = getenv('DB_USERNAME');
                $password = getenv('DB_PASSWORD');
                $dbname = getenv('DB_DATABASE');

                try {
                    DatabaseSingleton::$conn = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
                    DatabaseSingleton::$conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
                } catch (PDOException $e) {
                    echo "Connection failed: " . $e->getMessage();
                }
            }
        }

        public static function closeCon(){
            DatabaseSingleton::$conn = null;
        }
    }
