
import java.sql.ResultSet;
import java.sql.SQLException;

import org.springframework.jdbc.core.RowMapper;

public class [%ENTITY%]RowMapper implements RowMapper<[%ENTITY%]> {
 
    public [%ENTITY%] mapRow(ResultSet rs, int rowNum) throws SQLException {
        [%ENTITY%] [%ENTITYVAR%] = new [%ENTITY%]();

[%ROWMAPPER%]
 
        return [%ENTITYVAR%];
    }
}