// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "HSSurfaceViewer.generated.h"

UCLASS()
class OCULUSNEW_API AHSSurfaceViewer : public AActor
{
	GENERATED_BODY()
	
public:	
	// Sets default values for this actor's properties
	AHSSurfaceViewer();

protected:
	// Called when the game starts or when spawned
	virtual void BeginPlay() override;

public:	
	// Called every frame
	virtual void Tick(float DeltaTime) override;

	UPROPERTY(VisibleAnywhere)
	class UProceduralMeshComponent* ProceduralMeshComp;

	UPROPERTY(EditAnywhere)
	class UMaterialInstance* MaterialInstance = nullptr;

	UFUNCTION(BlueprintCallable)
	bool UpdateSurface();
};
