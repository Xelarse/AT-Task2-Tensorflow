using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using UnityEngine;

public class MapDataLoader : MonoBehaviour
{
    [SerializeField] private string jsonPath;

    [Header("Prefab references")]
    public GameObject cityPrefab;
    public GameObject densePrefab;
    public GameObject grassPrefab;
    public GameObject roadPrefab;
    public GameObject sandPrefab;
    public GameObject sparsePrefab;
    public GameObject villagePrefab;
    public GameObject waterPrefab;

    private MapTile[] mapTiles;

    private List<GameObject> levelTiles = new List<GameObject>();

    private float tileXSize = 5.0f;
    private float tileYSize = 5.0f;

    [ContextMenu("Load tiles from path")]
    private void loadTiles()
    {
        using (StreamReader stream = new StreamReader(jsonPath))
        {
            string json = stream.ReadToEnd();
            json = fixJson(json);
            mapTiles = JsonHelper.FromJson<MapTile>(json);
        }

        SetupMapViaLoadedData();
    }

    private void SetupMapViaLoadedData()
    {
        foreach (var tile in levelTiles)
        {
            Destroy(tile);
        }
        levelTiles.Clear();

        foreach (var tile in mapTiles)
        {
            GameObject newTile;

            switch (tile.Type)
            {
                case "City Building":
                    newTile = Instantiate(cityPrefab);
                    break;
                case "Dense Forest":
                    newTile = Instantiate(densePrefab);
                    break;
                case "Grass":
                    newTile = Instantiate(grassPrefab);
                    break;
                case "Road":
                    newTile = Instantiate(roadPrefab);
                    break;
                case "Sand":
                    newTile = Instantiate(sandPrefab);
                    break;
                case "Sparse Forest":
                    newTile = Instantiate(sparsePrefab);
                    break;
                case "Village Building":
                    newTile = Instantiate(villagePrefab);
                    break;
                default:
                    newTile = Instantiate(waterPrefab);
                    break;
            }

            Vector3 tilePos = Vector3.zero;
            tilePos.x = tile.XCord * tileXSize;
            tilePos.z = tile.YCord * tileYSize;

            newTile.transform.position = tilePos;
            levelTiles.Add(newTile);
        }
    }




    string fixJson(string value)
    {
        value = "{\"Items\":" + value + "}";
        return value;
    }
}
