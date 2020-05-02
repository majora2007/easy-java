public class [%ENTITY%]RowMapper implements RowMapper<[%ENTITY%]> {
 
    public [%ENTITY%] mapRow(ResultSet rs, int rowNum) throws SQLException {
        [%ENTITY%] [%ENTITYVAR%] = new [%ENTITY%]();

[%ROWMAPPER%]
 
        return [%ENTITYVAR%];
    }
}