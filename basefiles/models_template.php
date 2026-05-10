<?php

namespace App\Baseclasses;

use App\Controller\DatabaseController;

class Models
{
    public static function get(?int $id = null)
    {
        $parent = static::class;
        $parent = str_replace("App\\Models\\", "", $parent);

        $databasecontroller = new DatabaseController();

        if ($id != null) {
            $res = $databasecontroller->getFromTable($parent, true, true, "UsersID = $id");
        } else {
            $res = $databasecontroller->getFromTable($parent, true, false);
        }

        return $res;
    }
}
