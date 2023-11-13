using Npgsql;

public class AnimalService
{
    private readonly string? _connectionString;

    public AnimalService(IConfiguration configuration)
    {
        _connectionString = configuration.GetConnectionString("DefaultConnection");
    }

    // Fetch a single animal by its ID
    public Animal GetAnimalById(int id)
    {
        Animal? animal = null;

        using (NpgsqlConnection connection = new NpgsqlConnection(_connectionString))
        {
            connection.Open();
            using (NpgsqlCommand cmd = new NpgsqlCommand("SELECT * FROM Animals WHERE Id = @Id", connection))
            {
                cmd.Parameters.AddWithValue("@Id", id);
                using (NpgsqlDataReader reader = cmd.ExecuteReader())
                {
                    if (reader.Read())
                    {
                        animal = new Animal
                        {
                            Id = reader.GetInt32(reader.GetOrdinal("Id")),
                            RescueCentre = reader.GetString(reader.GetOrdinal("RescueCentre")),
                            Breed = reader.GetString(reader.GetOrdinal("Breed")),
                            ImageUrl = reader.GetString(reader.GetOrdinal("ImageUrl")),
                            Adoptable = reader.GetBoolean(reader.GetOrdinal("Adoptable"))
                        };
                    }
                    else
                    {
                        throw new InvalidOperationException($"No animal found with the provided ID: {id}");
                    }
                }
            }
        }

        return animal;
    }

    // Add a new animal
    public void AddAnimal(Animal animal)
    {
        using (NpgsqlConnection connection = new NpgsqlConnection(_connectionString))
        {
            connection.Open();
            using (NpgsqlCommand cmd = new NpgsqlCommand("INSERT INTO Animals (RescueCentre, Breed, ImageUrl, Adoptable) VALUES (@RescueCentre, @Breed, @ImageUrl, @Adoptable)", connection))
            {
                cmd.Parameters.AddWithValue("@RescueCentre", animal.RescueCentre);
                cmd.Parameters.AddWithValue("@Breed", animal.Breed);
                cmd.Parameters.AddWithValue("@ImageUrl", animal.ImageUrl);
                cmd.Parameters.AddWithValue("@Adoptable", animal.Adoptable);

                cmd.ExecuteNonQuery();
            }
        }
    }

    // Update the Adoptable status of an animal
    public void UpdateAdoptableStatus(int animalId, bool adoptableStatus)
    {
        using (NpgsqlConnection connection = new NpgsqlConnection(_connectionString))
        {
            connection.Open();
            using (NpgsqlCommand cmd = new NpgsqlCommand("UPDATE Animals SET Adoptable = @Adoptable WHERE Id = @Id", connection))
            {
                cmd.Parameters.AddWithValue("@Id", animalId);
                cmd.Parameters.AddWithValue("@Adoptable", adoptableStatus);

                cmd.ExecuteNonQuery();
            }
        }
    }

    // Delete an animal by its ID
    public void DeleteAnimal(int id)
    {
        using (NpgsqlConnection connection = new NpgsqlConnection(_connectionString))
        {
            connection.Open();
            using (NpgsqlCommand cmd = new NpgsqlCommand("DELETE FROM Animals WHERE Id = @Id", connection))
            {
                cmd.Parameters.AddWithValue("@Id", id);
                cmd.ExecuteNonQuery();
            }
        }
    }
}
