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
        LinkRelatedTiles();
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

        return;
    }

    private void LinkRelatedTiles()
    {
        int startX, endX, startY, endY;
        startX = startY = endX = endY = 0;

        //loop through to get the max row and max col
        foreach (var tileData in mapTiles)
        {
            endX = tileData.XCord > endX ? tileData.XCord : endX;
            endY = tileData.YCord > endY ? tileData.YCord : endY;
        }

        endX++;
        endY++;

        //Scan through each tile checking the cardinal directions and if so setting the current tile in question to do stuff
        for (int i = 0; i < levelTiles.Count; i++)
        {
            GameObject tile = levelTiles[i];
            MapTileConfigurer tileScript = tile.GetComponent<MapTileConfigurer>();

            if (tileScript != null)
            {
                //First get the co-ords of the current position
                int centerTileX = i % endX;
                int centerTileY = Mathf.FloorToInt(i / endX);

                //bool left = IsTileTypeMatching(centerTileX - 1, centerTileY, endX, endY, tileScript._tileType);
                //bool right = IsTileTypeMatching(centerTileX + 1, centerTileY, endX, endY, tileScript._tileType);
                //bool top = IsTileTypeMatching(centerTileX, centerTileY + 1, endX, endY, tileScript._tileType);
                //bool bot = IsTileTypeMatching(centerTileX, centerTileY - 1, endX, endY, tileScript._tileType);

                bool left = IsTileTypeMatching(centerTileX, centerTileY - 1, endX, endY, tileScript._tileType);
                bool right = IsTileTypeMatching(centerTileX, centerTileY + 1, endX, endY, tileScript._tileType);
                bool top = IsTileTypeMatching(centerTileX - 1, centerTileY, endX, endY, tileScript._tileType);
                bool bot = IsTileTypeMatching(centerTileX + 1, centerTileY, endX, endY, tileScript._tileType);

                switch (tileScript._tileType)
                {
                    case MapTileConfigurer.Tile.CITY_BUILDING:
                    case MapTileConfigurer.Tile.VILLAGE_BUILDING:
                        tileScript.InitTile(GetBuildingConfig(top, bot, left, right));
                        break;
                    case MapTileConfigurer.Tile.ROAD:
                        tileScript.InitTile(GetRoadConfig(top, bot, left, right));
                        break;
                }
            }
        }
    }

    private MapTileConfigurer.TileConfig GetBuildingConfig(bool top, bool bottom, bool left, bool right)
    {
        if(left && right)
        {
            return MapTileConfigurer.TileConfig.LR;
        }
        else if (left)
        {
            return MapTileConfigurer.TileConfig.L;
        }
        else if (right)
        {
            return MapTileConfigurer.TileConfig.R;
        }
        else if(top && bottom)
        {
            return MapTileConfigurer.TileConfig.TB;
        }
        else if (top)
        {
            return MapTileConfigurer.TileConfig.T;
        }
        else if (bottom)
        {
            return MapTileConfigurer.TileConfig.B;
        }
        else
        {
            return MapTileConfigurer.TileConfig.SINGLE;
        }
    }

    private MapTileConfigurer.TileConfig GetRoadConfig(bool top, bool bottom, bool left, bool right)
    {
        if(top && bottom && left && right)
        {
            return MapTileConfigurer.TileConfig.TRBL;
        }
        else if (bottom && left && top)
        {
            return MapTileConfigurer.TileConfig.BLT;
        }
        else if (left && bottom && right)
        {
            return MapTileConfigurer.TileConfig.RBL;
        }
        else if (top && right && bottom)
        {
            return MapTileConfigurer.TileConfig.TRB;
        }
        else if (left && top && right)
        {
            return MapTileConfigurer.TileConfig.LTR;
        }
        else if (bottom && right)
        {
            return MapTileConfigurer.TileConfig.BR;
        }
        else if(bottom && left)
        {
            return MapTileConfigurer.TileConfig.BL;
        }
        else if (top && right)
        {
            return MapTileConfigurer.TileConfig.TR;
        }
        else if (top && left)
        {
            return MapTileConfigurer.TileConfig.TL;
        }
        else
        {
            return GetBuildingConfig(top, bottom, left, right);
        }
    }

    private bool IsTileTypeMatching(int x, int y, int xMax, int yMax, MapTileConfigurer.Tile tileType)
    {
        //safety checks first
        if(x >= xMax || x < 0) { return false; }
        if(y >= yMax || y < 0) { return false; }

        //Get the index, and compare type
        MapTileConfigurer tile = levelTiles[xMax * y + x].GetComponent<MapTileConfigurer>();
        if(tile == null) { return false; }
        return tile._tileType == tileType;
    }

    string fixJson(string value)
    {
        value = "{\"Items\":" + value + "}";
        return value;
    }
}
